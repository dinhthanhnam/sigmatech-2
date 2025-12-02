from sqlmodel import Field, Relationship
from typing import Optional, List, Type, Self, Sequence, TypeVar
from .base import Base, SQLModel, Session
from utils.crypto import hash
from sqlalchemy.exc import IntegrityError
from exceptions.models.unique_constraint import UniqueConstraintError


T = TypeVar("T", bound="Test")


class Test(Base, table=True):
    __tablename__ = "test" # type: ignore
    name: str = Field(default=None)