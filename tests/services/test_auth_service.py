import hashlib
import hmac
import time
from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException
from starlette.requests import Request

from app.schemes.tg_scheme import InitData, User
from app.services.auth_service import AuthService


def make_request(path: str, headers: dict[str, str]) -> Request:
    raw_headers = [(k.encode(), v.encode()) for k, v in headers.items()]
    scope = {
        "type": "http",
        "method": "GET",
        "path": path,
        "headers": raw_headers,
    }
    return Request(scope)


def sign_payload(token: str, payload: dict[str, str]) -> str:
    data_check = payload.copy()
    data_check.pop("hash", None)
    sorted_items = sorted(data_check.items())
    data_check_string = "\n".join([f"{k}={v}" for k, v in sorted_items])

    secret_key = hmac.new(
        key=b"WebAppData", msg=token.encode(), digestmod=hashlib.sha256
    ).digest()
    return hmac.new(
        key=secret_key, msg=data_check_string.encode(), digestmod=hashlib.sha256
    ).hexdigest()


def test_parse_telegram_init_data():
    parsed = AuthService._parse_telegram_init_data("a=1&b=hello%20world")

    assert parsed == {"a": "1", "b": "hello world"}


def test_validate_tg_hash_bypasses_health():
    request = make_request("/health", {})

    assert AuthService.validate_tg_hash(request) is True


def test_validate_tg_hash_invalid_header():
    request = make_request("/auth/init", {})

    with pytest.raises(HTTPException) as exc:
        AuthService.validate_tg_hash(request)

    assert exc.value.status_code == 401


def test_validate_telegram_webapp_data_valid(monkeypatch):
    monkeypatch.setattr("app.services.auth_service.BOT_TOKEN", "token")
    now = int(time.time())
    payload = {"auth_date": str(now), "query_id": "1", "hash": ""}
    payload["hash"] = sign_payload("token", payload)

    assert AuthService._validate_telegram_webapp_data(payload) is True


@pytest.mark.anyio
async def test_init_returns_existing_user():
    user_service = AsyncMock()
    user_service.get_by_tg_id.return_value = {"id": 1}
    service = AuthService(user_service=user_service)
    data = InitData(
        user=User(
            id=1,
            username="alice",
            first_name="Alice",
            last_name="A",
            language_code="en",
            photo_url="https://example.com/photo.png",
        ),
        auth_date=datetime(2024, 1, 1, tzinfo=timezone.utc),
        hash="dummy",
    )

    result = await service.init(data)

    assert result == {"id": 1}
    user_service.create.assert_not_called()


@pytest.mark.anyio
async def test_init_creates_user_when_missing():
    user_service = AsyncMock()
    user_service.get_by_tg_id.return_value = None
    user_service.create.return_value = {"id": 2}
    service = AuthService(user_service=user_service)
    data = InitData(
        user=User(
            id=2,
            username="bob",
            first_name="Bob",
            last_name="B",
            language_code="en",
            photo_url="https://example.com/photo.png",
        ),
        auth_date=datetime(2024, 1, 1, tzinfo=timezone.utc),
        hash="dummy",
    )

    result = await service.init(data)

    assert result == {"id": 2}
    user_service.create.assert_awaited_once()
    created = user_service.create.await_args.args[0]
    assert created.tg_id == "2"
    assert created.login == "bob"
    assert created.name == "Bob"
