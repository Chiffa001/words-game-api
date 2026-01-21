from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    # SQLAlchemy declarative base intentionally has no public methods.
    # pylint: disable=too-few-public-methods
    __abstract__ = True
