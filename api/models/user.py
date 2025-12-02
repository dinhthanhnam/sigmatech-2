from sqlmodel import Field, Relationship
from typing import Optional, List, Type, Self, Sequence, TypeVar
from .base import Base, SQLModel, Session
from utils.crypto import hash
from sqlalchemy.exc import IntegrityError
from exceptions.models.unique_constraint import UniqueConstraintError


T = TypeVar("T", bound="User")


class User(Base, table=True):
    __tablename__ = "users" # type: ignore
    
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False

    posts: List["Post"] = Relationship(back_populates="author") # type: ignore


    @classmethod
    def find_by_email(cls: Type[T], email: str) -> Optional[T]:
        return cls.query().where(cls.email == email).first()


    @classmethod
    def find_by_username(cls: Type[T], username: str) -> Optional[T]:
        return cls.query().where(cls.username == username).first()


    # override
    @classmethod
    def create(cls: Type[T], data: SQLModel | dict) -> Optional[T]:
        payload = data.model_dump() if isinstance(data, SQLModel) else data
        payload["hashed_password"] = hash(payload.pop("password"))
        try:
            return super().create(payload)
        except IntegrityError as e:
            msg = str(e.orig)
            if "Duplicate entry" in msg:
                raise UniqueConstraintError(msg)

    # override
    @classmethod
    def create_many(cls: Type[T], data_list: list[SQLModel] | list[dict]) -> Sequence[T]:
        payload = []
        for data in data_list:
            item = data.model_dump() if isinstance(data, SQLModel) else dict(data)
            item["hashed_password"] = hash(item.pop("password"))
            payload.append(item)

        return super().create_many(payload)