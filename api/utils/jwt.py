from datetime import datetime, timedelta
from jose import jwt
from typing import Optional
import uuid
from core.config import settings


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None):
    now = datetime.now()
    exp = now + (expires_delta or timedelta(minutes=settings.at_expire_mins)) # type: ignore
    payload = {
        "sub": subject,
        "exp": exp,
        "iat": now,
        "typ": "access",
        "jti": str(uuid.uuid4())
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm) # type: ignore

def create_refresh_token(subject: str, expires_delta: Optional[timedelta] = None):
    now = datetime.now()
    exp = now + (expires_delta or timedelta(days=settings.rt_expire_day)) # type: ignore
    payload = {
        "sub": subject,
        "exp": exp,
        "iat": now,
        "typ": "refresh",
        "jti": str(uuid.uuid4())
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm) # type: ignore

def decode_token(token: str):
    return jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm]) # type: ignore