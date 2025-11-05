from typing import Optional
from .base import BaseSchema, BaseReadSchema, BaseUpdateSchema
from pydantic import Field, EmailStr
from utils.constants import Description, Example

class UserCreate(BaseSchema):
    username: str = Field(..., description=Description.User.username, examples=Example.User.username, min_length=8, max_length=20)
    email: EmailStr = Field(..., description=Description.User.email, examples=Example.User.email)
    password: str = Field(..., description=Description.User.password, examples=Example.User.password, min_length=8, max_length=20)


class UserRead(BaseReadSchema):
    id: int
    username: str
    email: str
    is_active: bool
    is_superuser: bool

class PartialUser(BaseSchema):
    username: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None

class UserUpdate(BaseUpdateSchema, PartialUser):
    pass

class UserAuth(BaseSchema):
    email: EmailStr = Field(..., description=Description.User.email, examples=Example.User.email)
    password: str = Field(..., description=Description.User.password, examples=Example.User.password, min_length=8, max_length=20)