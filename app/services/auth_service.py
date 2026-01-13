from fastapi import Depends

from app.schemes.user_scheme import UserCreateScheme, UserInitScheme
from app.services.user_service import UserService


class AuthService:
    def __init__(self, user_service: UserService = Depends(UserService)) -> None:
        self.user_service = user_service

    async def init(self, user: UserInitScheme):
        existed_user = await self.user_service.get_by_tg_id(tg_id=user.tg_id)

        if existed_user is not None:
            return existed_user

        return await self.user_service.create(UserCreateScheme(**user.dict()))
