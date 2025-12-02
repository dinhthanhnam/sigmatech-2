from sqlmodel import Field, Relationship
from typing import Optional, List, Type, Sequence, TypeVar
from .base import Base
from datetime import datetime

T = TypeVar("T", bound="RefreshToken")

class RefreshToken(Base, table=True):
    __tablename__ = "refresh_tokens" # type: ignore

    user_id: int = Field(foreign_key="users.id", nullable=False, index=True)
    jti: str = Field(unique=True, index=True)
    token_hash: str
    expires_at: datetime
    revoked: bool = False
    replaced_by_jti: Optional[str] = None

    @classmethod
    def find_by_jti(cls: Type[T], jti: str) -> Optional[T]:
        """Find refresh token by JWT ID"""
        return cls.query().where(cls.jti == jti).first()

    @classmethod
    def find_by_user_id(cls: Type[T], user_id: int) -> Sequence[T]:
        """Find all refresh tokens for a user"""
        return cls.query().where(cls.user_id == user_id).all()
