from fastapi import APIRouter, Depends, HTTPException, status
from schemas.user import UserRead
from services.impl.user_service_impl import user_service
from typing import List
from schemas.user import UserCreate, UserUpdate, UserAuth
from models import User
from typing import Annotated
from middlewares import get_current_user
from i18n import t
from exceptions import UniqueConstraintError
from utils.jwt import create_access_token, create_refresh_token

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
    payload: UserAuth
):
    user = user_service.authenticate_user(payload)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= t('common.user.not_found')
        )
    create_access_token(user.id)
    create_refresh_token(user.id)

    return user
    

@router.get(path='/refresh')
def refresh():
    return
