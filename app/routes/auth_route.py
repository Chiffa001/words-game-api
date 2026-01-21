from fastapi import APIRouter, Depends

from app.schemes.tg_scheme import InitData
from app.schemes.user_scheme import UserOutScheme
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/init", response_model=UserOutScheme)
async def init(
    data: InitData,
    auth_service: AuthService = Depends(AuthService),
):
    return await auth_service.init(data)
