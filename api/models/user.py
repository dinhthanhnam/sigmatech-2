from sqlmodel import Field, Relationship
from datetime import datetime, UTC
from typing import Optional, List
from .base import Base


class User(Base, table=True):
    __tablename__ = "users" # type: ignore
    
    username: str
    email: Optional[str] = None
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False

    posts: List["Post"] = Relationship(back_populates="author") # type: ignore


