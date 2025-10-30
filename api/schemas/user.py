from typing import Optional
from .base import BaseSchema


class UserCreate(BaseSchema):
    username: str
    email: Optional[str] = None
    password: str


class UserRead(BaseSchema):
    id: int
    username: str
    email: str
    is_active: bool
    is_superuser: bool


class UserUpdate(BaseSchema):
    username: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None