from unittest.mock import AsyncMock, MagicMock

import pytest

from app.repositories.user_repository import UserRepository
from app.schemes.user_scheme import UserCreateScheme


@pytest.mark.anyio
async def test_create_user_persists():
    session = AsyncMock()
    session.add = MagicMock()
    repo = UserRepository(db=session)

    async def set_id(obj):
        obj.id = 1

    session.refresh = AsyncMock(side_effect=set_id)

    created = await repo.create(
        UserCreateScheme(tgId="tg-123", login="alice", name="Alice")
    )

    session.add.assert_called_once_with(created)
    session.commit.assert_awaited_once()
    session.refresh.assert_awaited_once_with(created)

    assert created.id == 1
    assert created.tg_id == "tg-123"
    assert created.login == "alice"
    assert created.name == "Alice"

@pytest.mark.anyio
async def test_get_by_tg_id_returns_user():
    session = AsyncMock()
    result = MagicMock()
    user = MagicMock()
    result.scalars.return_value.first.return_value = user
    session.execute = AsyncMock(return_value=result)

    repo = UserRepository(db=session)
    fetched = await repo.get_by_tg_id("tg-123")

    session.execute.assert_awaited_once()
    assert fetched is user


@pytest.mark.anyio
async def test_get_by_tg_id_missing_returns_none():
    session = AsyncMock()
    result = MagicMock()
    result.scalars.return_value.first.return_value = None
    session.execute = AsyncMock(return_value=result)

    repo = UserRepository(db=session)
    fetched = await repo.get_by_tg_id("missing")

    session.execute.assert_awaited_once()
    assert fetched is None
