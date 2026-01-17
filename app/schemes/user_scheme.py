from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UserBaseScheme(BaseModel):
    tg_id: str = Field(alias="tgId")
    name: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)


class UserCreateScheme(UserBaseScheme):
    login: str


class UserOutScheme(UserBaseScheme):
    model_config = ConfigDict(from_attributes=True)
