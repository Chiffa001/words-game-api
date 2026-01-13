from fastapi import APIRouter, Depends

from app.schemes.user_scheme import UserInitScheme, UserOutScheme
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/init", response_model=UserOutScheme)
async def init(
    user: UserInitScheme,
    auth_service: AuthService = Depends(AuthService),
):
    response = await auth_service.init(user)
    return response
