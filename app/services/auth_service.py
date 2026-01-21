import hashlib
import hmac
import time
import traceback
from typing import Dict
from urllib.parse import parse_qs, unquote

from fastapi import Depends, Request, status
from fastapi.exceptions import HTTPException

from app.core.config import BOT_TOKEN
from app.schemes.tg_scheme import InitData
from app.schemes.user_scheme import UserCreateScheme
from app.services.user_service import UserService


class AuthService:
    def __init__(self, user_service: UserService = Depends(UserService)) -> None:
        self.user_service = user_service

    @staticmethod
    def _parse_telegram_init_data(init_data_str: str) -> Dict[str, str]:
        parsed = parse_qs(init_data_str)

        result = {}
        for key, value in parsed.items():
            if value:
                decoded_value = unquote(value[0])
                result[key] = decoded_value

        return result

    @staticmethod
    def _validate_telegram_webapp_data(init_data: Dict[str, str]) -> bool:
        try:
            required_fields = ["auth_date", "hash"]
            for field in required_fields:
                if field not in init_data:
                    raise ValueError("Missing required field")

            received_hash = init_data["hash"]

            data_check = init_data.copy()
            data_check.pop("hash", None)

            sorted_items = sorted(data_check.items())

            data_check_string = "\n".join([f"{k}={v}" for k, v in sorted_items])

            secret_key = hmac.new(
                key=b"WebAppData", msg=BOT_TOKEN.encode(), digestmod=hashlib.sha256
            ).digest()

            computed_hash = hmac.new(
                key=secret_key, msg=data_check_string.encode(), digestmod=hashlib.sha256
            ).hexdigest()

            if not hmac.compare_digest(computed_hash, received_hash):
                raise ValueError("Hash comparison failed")

            auth_date = int(init_data.get("auth_date", 0))
            current_time = int(time.time())

            if current_time - auth_date > 86400:  # 24 hours
                print(f"Auth expired. Auth date: {auth_date}, Current: {current_time}")
                raise ValueError("Auth expired")

            return True

        except Exception as exc:
            print(f"Validation error: {exc}")
            traceback.print_exc()
            raise ValueError("Validation error") from exc

    @staticmethod
    def validate_tg_hash(request: Request) -> bool:
        if request.url.path.startswith("/health"):
            return True

        try:
            init_data_str = request.headers.get("x-tg-hash")

            if init_data_str is None:
                raise ValueError("Header tg-has is required")

            parsed = AuthService._parse_telegram_init_data(init_data_str)
            AuthService._validate_telegram_webapp_data(parsed)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid payload"
            ) from exc

        return True

    async def init(self, init_data: InitData):
        existed_user = await self.user_service.get_by_tg_id(
            tg_id=str(init_data.user.id)
        )

        if existed_user is not None:
            return existed_user

        return await self.user_service.create(
            UserCreateScheme(
                tgId=str(init_data.user.id),
                name=init_data.user.first_name,
                login=init_data.user.username,
            )
        )
