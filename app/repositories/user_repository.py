from fastapi import Depends
from sqlalchemy import select

from app.models.user_model import UserModel
from app.schemes.user_scheme import UserCreateScheme
from app.services.db_service import get_db


class UserRepository:
    def __init__(self, db=Depends(get_db)):
        self.db_session = db

    async def create(self, new_user: UserCreateScheme) -> UserModel:
        user = UserModel(login=new_user.login, name=new_user.name, tg_id=new_user.tg_id)
        self.db_session.add(user)
        await self.db_session.commit()
        await self.db_session.refresh(user)
        return user

    async def get_by_tg_id(self, tg_id: str) -> UserModel | None:
        result = await self.db_session.execute(
            select(UserModel).where(UserModel.tg_id == tg_id)
        )
        return result.scalars().first()
