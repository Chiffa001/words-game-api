from sqlalchemy import Integer, String, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True)
    tg_id: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False)
    login: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String)
    created_at: Mapped[str] = mapped_column(
        DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[str] = mapped_column(
        DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'))
