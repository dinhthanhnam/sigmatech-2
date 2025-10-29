from sqlmodel import Field, Relationship
from typing import Optional
from .base import Base


class Post(Base, table=True):
    __tablename__ = "posts" # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    author_id: int = Field(foreign_key="users.id")

    author: Optional["User"] = Relationship(back_populates="posts") # type: ignore
