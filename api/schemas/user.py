from typing import Optional
from .base import BaseSchema


class UserCreate(BaseSchema):
    username: str
    email: Optional[str] = None
    password: str


class UserRead(BaseSchema):
    id: int
    username: str
    email: Optional[str] = None
    is_active: bool
    is_superuser: bool