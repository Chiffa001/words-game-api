from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from app.routes import auth_route, healthmonitor_route
from app.services.auth_service import AuthService


def build_app() -> FastAPI:
    app = FastAPI(dependencies=[Depends(AuthService.validate_tg_hash)])
    app.include_router(auth_route.router)
    app.include_router(healthmonitor_route.router)
    return app


def test_auth_init_returns_user():
    app = build_app()
    auth_mock = AsyncMock()
    auth_mock.init.return_value = SimpleNamespace(tg_id="tg-1", name="Alice")
    app.dependency_overrides[AuthService] = lambda: auth_mock
    app.dependency_overrides[AuthService.validate_tg_hash] = lambda: True

    payload = {
        "user": {
            "id": 1,
            "username": "alice",
            "first_name": "Alice",
            "last_name": "A",
            "language_code": "en",
            "photo_url": "https://example.com/photo.png",
        },
        "auth_date": datetime(2024, 1, 1, tzinfo=timezone.utc).isoformat(),
        "hash": "dummy",
    }

    with TestClient(app) as client:
        response = client.post("/auth/init", json=payload)

    assert response.status_code == 200
    assert response.json() == {"tgId": "tg-1", "name": "Alice"}
    auth_mock.init.assert_awaited_once()
