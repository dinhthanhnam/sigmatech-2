from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from utils.jwt import decode_token
from jose import JWTError
from models import User
from deps import authorization_header
from i18n import t
from typing import Annotated


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(authorization_header)]
) -> User:
    token = credentials.credentials
    try:
        payload = decode_token(token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=t('common.token.invalid')
        )

    user = User.find_by_id(payload["sub"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=t('common.user.not_found')
        )

    return user