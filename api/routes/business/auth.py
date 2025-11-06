from fastapi import APIRouter, Depends, HTTPException, status, Response
from services import user_service
from typing import List
from schemas import UserCreate, UserRead, UserUpdate, UserAuthRequest
from models import User
from typing import Annotated
from middlewares import get_current_user
from i18n import t
from exceptions import UniqueConstraintError
from utils.jwt import create_access_token, create_refresh_token, decode_token
from core.config import settings
from exceptions import PasswordMismatchedError

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get(path='/profile',response_model=UserRead)
def get_profile(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user


@router.post(path='/register', response_model=UserRead)
def register_user(
    payload: UserCreate
):
    try:
        return user_service.create_user(payload)
    except Exception as e:
        if isinstance(e, UniqueConstraintError):
            if e.field == 'email':
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail= t('common.user.email_existed')
                )
            elif e.field == 'username':
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=t('common.user.username_existed')
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=t('common.bad_request')
                )


@router.post(path='/login', response_model=UserRead)
def authenticate_user(
    payload: UserAuthRequest,
    response: Response
):
    try:
        user = user_service.authenticate_user(payload)
        access_token = create_access_token(user.id) # type: ignore
        refresh_token = create_refresh_token(user.id) # type: ignore

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=60*60*24*(settings.rt_expire_days or 7)
        )
        
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=False,
            secure=True,
            samesite="lax",
            max_age=60*(settings.at_expire_mins or 15)
        )

        return user
    except PasswordMismatchedError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e
        )


@router.get(path='/refresh')
def refresh():
    return
