from fastapi import APIRouter, Query, Depends, Request
from models.user import User
from schemas.user import UserRead
from services.impl.user_service_impl import user_service
from typing import List
from schemas.user import UserCreate, UserUpdate
from core.security import ApiBindingScope, AuthManager
from exceptions import UnauthorizedError
from fastapi import HTTPException, status
from i18n import t

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(path='/',response_model=List[UserRead], dependencies=[Depends(AuthManager(ApiBindingScope.SUPERUSER_ONLY))])
def index(request: Request, page: int = Query(1, ge=1)):
    return user_service.get_paginated_users(page=page, take=8)


@router.get(path='/{id}',response_model=UserRead)
def show(id: int):
    return user_service.get_user_by_id(id)


@router.post(path='/',response_model=UserRead)
def store(payload: UserCreate):
    return user_service.create_user(payload)


@router.patch('/{id}', response_model=UserRead, dependencies=[Depends(AuthManager(ApiBindingScope.BIND_TO_USER, model_to_bind=User, key_to_bind="id"))])
def update(id: int, payload: UserUpdate, request: Request):
    make_superuser_request = getattr(payload, "is_superuser", None)
    # If not a superuser creation/update request, proceed normally
    if not make_superuser_request:
        return user_service.update_user(id, payload)
    # For superuser creation/update, ensure the requester is a superuser
    user: User = request.state.user
    if not user.is_superuser:
        raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f'{t("common.auth.forbidden")}',
        )

    return user_service.update_user(id, payload)
        
    


@router.delete('/{id}', response_model=UserRead, dependencies=[Depends(AuthManager(ApiBindingScope.SUPERUSER_ONLY))])
def destroy(id: int):
    return user_service.delete_user(id)