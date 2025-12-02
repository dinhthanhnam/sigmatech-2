from fastapi import APIRouter, Query, Depends, Request
from schemas.user import UserRead
from services.impl.user_service_impl import user_service
from typing import List
from schemas.user import UserCreate, UserUpdate
from core.security import AuthManager

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(path='/',response_model=List[UserRead], dependencies=[Depends(AuthManager())])
def index(request: Request, page: int = Query(1, ge=1)):
    # print(request.state.user)
    return user_service.get_paginated_users(page=page, take=8)


@router.get(path='/{user_id}',response_model=UserRead)
def show(user_id: int):
    return user_service.get_user_by_id(user_id)


@router.post(path='/',response_model=UserRead)
def store(payload: UserCreate):
    return user_service.create_user(payload)


@router.patch('/{user_id}', response_model=UserRead)
def update(user_id: int, payload: UserUpdate):
    return user_service.update_user(user_id, payload)


@router.delete('/{user_id}', response_model=UserRead)
def destroy(user_id: int):
    return user_service.delete_user(user_id)