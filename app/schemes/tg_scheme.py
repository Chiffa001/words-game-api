from datetime import datetime, timezone

from pydantic import BaseModel, field_validator


class User(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    language_code: str
    photo_url: str


class InitData(BaseModel):
    user: User
    auth_date: datetime
    hash: str

    @field_validator("auth_date")
    @classmethod
    def must_be_utc(cls, v: datetime):
        if v.tzinfo != timezone.utc:
            raise ValueError("auth_date must be utc")
        return v
