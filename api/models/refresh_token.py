from sqlmodel import Field, Relationship
from typing import Optional, List
from .base import Base
from datetime import datetime

class RefreshToken(Base, table=True):
    __tablename__ = "refresh_tokens" # type: ignore

    user_id: int = Field(foreign_key="users.id", nullable=False, index=True)
    jti: str
    token_hash: str
    expires_at: datetime
    revoked: bool = False
    replaced_by_jti: Optional[str] = None
