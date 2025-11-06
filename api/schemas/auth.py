from typing import Optional
from .base import BaseSchema
from pydantic import Field, EmailStr
from utils.constants import Description, Example


class UserAuthRequest(BaseSchema):
    email: EmailStr = Field(..., description=Description.User.email, examples=Example.User.email)
    password: str = Field(..., description=Description.User.password, examples=Example.User.password, min_length=8, max_length=20)