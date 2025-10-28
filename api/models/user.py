from sqlmodel import Field, Relationship
from datetime import datetime, UTC
from typing import Optional, List
from .base import Base


class UserBase(Base):
    username: str
    email: Optional[str] = None


class User(UserBase, table=True):
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime = Field(default=datetime.now(UTC))

    posts: List["Post"] = Relationship(back_populates="author") #type: ignore


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    is_active: bool
    is_superuser: bool
