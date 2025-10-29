from typing import Optional
from .user import UserRead
from .base import BaseSchema

class Post(BaseSchema):
    id: int
    title: str
    content: str


class PostRead(Post):
    author_id: int


class PostWithUserRead(Post):
    author: UserRead