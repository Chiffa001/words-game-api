from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

from app.schemes.user_scheme import UserCreateScheme
from app.services.user_service import UserService


@pytest.mark.anyio
async def test_get_by_tg_id_delegates_to_repository():
    repo = AsyncMock()
    repo.get_by_tg_id.return_value = {"id": 1}

    service = UserService(user_repository=repo)
    result = await service.get_by_tg_id("tg-1")

    repo.get_by_tg_id.assert_awaited_once_with(tg_id="tg-1")
    assert result == {"id": 1}


@pytest.mark.anyio
async def test_create_raises_when_user_exists():
    repo = AsyncMock()
    repo.get_by_tg_id.return_value = {"id": 1}

    service = UserService(user_repository=repo)

    with pytest.raises(HTTPException) as exc:
        await service.create(
            UserCreateScheme(tgId="tg-1", login="alice", name="Alice")
        )

    assert exc.value.status_code == 409
    repo.create.assert_not_called()


@pytest.mark.anyio
async def test_create_creates_when_missing():
    repo = AsyncMock()
    repo.get_by_tg_id.return_value = None
    repo.create.return_value = {"id": 2}

    service = UserService(user_repository=repo)
    payload = UserCreateScheme(tgId="tg-2", login="bob", name="Bob")
    result = await service.create(payload)

    repo.get_by_tg_id.assert_awaited_once_with(tg_id="tg-2")
    repo.create.assert_awaited_once_with(new_user=payload)
    assert result == {"id": 2}
