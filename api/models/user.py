from sqlmodel import Field, Relationship
from typing import Optional, List
from .base import Base


class User(Base, table=True):
    __tablename__ = "users" # type: ignore
    
    username: str = Field(index=True, unique=True)
    email: str = Field(unique=True)
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False

    posts: List["Post"] = Relationship(back_populates="author") # type: ignore
