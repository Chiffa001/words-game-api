from fastapi import Depends, HTTPException, status

from app.repositories.user_repository import UserRepository
from app.schemes.user_scheme import UserCreateScheme


class UserService:
    def __init__(
        self, user_repository: UserRepository = Depends(UserRepository)
    ) -> None:
        self.user_repository = user_repository

    async def get_by_tg_id(self, tg_id: str):
        return await self.user_repository.get_by_tg_id(tg_id=tg_id)

    async def create(self, new_user: UserCreateScheme):
        is_user_exists = (await self.get_by_tg_id(tg_id=new_user.tg_id)) is not None

        if is_user_exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Such user already exists"
            )

        return await self.user_repository.create(new_user=new_user)
