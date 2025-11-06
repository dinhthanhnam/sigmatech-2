from services.user_service import UserService
from models import User
from typing import Sequence, Optional
from schemas import UserCreate, UserUpdate, UserAuthRequest
from utils.crypto import verify_password
from exceptions import PasswordMismatchedError

class UserServiceImpl(UserService):


    @classmethod
    def get_all_users(cls) -> Sequence[User]:
        return User.query().all()


    @classmethod
    def get_paginated_users(cls, page: int, take: int) -> Sequence[User]:
        offset = (page - 1) * take
        return User.query().offset(offset).limit(take).all()


    @classmethod
    def get_user_by_id(cls, id: int) -> Optional[User]:
        return User.find_by_id(id)


    @classmethod
    def create_user(cls, payload: UserCreate | dict) -> User | None:
        return User.create(payload)


    @classmethod
    def update_user(cls, id, payload: UserUpdate | dict) -> User | None:
        return User.update(id, payload)


    @classmethod
    def delete_user(cls, id) -> User | None:
        return User.delete_soft(id)

    #------------Bussiness--------------
    #------------Auth-------------------
    @classmethod
    def authenticate_user(cls, payload: UserAuthRequest) -> User | None:
        user = User.find_by_email(payload.email)
        if not user:
            raise UserNotFoundError()
        password_matched = verify_password(payload.password, user.hashed_password)
        if not password_matched:
            raise PasswordMismatchedError()
        return user


user_service = UserServiceImpl()