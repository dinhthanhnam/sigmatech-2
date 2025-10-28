from sqlmodel import Field, Relationship
from typing import Optional
from .base import Base


class Post(Base, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    author_id: int = Field(foreign_key="user.id")

    author: Optional["User"] = Relationship(back_populates="posts") # type: ignore
