from sqlmodel import Field, Relationship
from typing import Optional, List, Type
from .base import Base, T, SQLModel, Session
from utils.crypto import hash


class User(Base, table=True):
    __tablename__ = "users" # type: ignore
    
    username: str = Field(index=True, unique=True)
    email: str = Field(unique=True)
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False

    posts: List["Post"] = Relationship(back_populates="author") # type: ignore

    # override
    @classmethod
    def create(cls: Type[T], data: SQLModel | dict, sess: Session | None = None) -> T:
        payload = data.model_dump() if isinstance(data, SQLModel) else data
        payload["hashed_password"] = hash(payload.pop("password"))
        return super().create(payload, sess)


    @classmethod
    def create_many(cls: Type[T], data_list: list[SQLModel] | list[dict], sess: Session | None = None):
        payload = []
        for data in data_list:
            item = data.model_dump() if isinstance(data, SQLModel) else dict(data)
            item["hashed_password"] = hash(item.pop("password"))
            payload.append(item)

        return super().create_many(payload, sess)