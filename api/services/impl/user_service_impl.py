from services.user_service import UserService
from services import User
from typing import Sequence, Optional
from schemas.user import UserCreate, UserUpdate


class UserServiceImpl(UserService):

    
    @classmethod
    def get_all_users(cls) -> Sequence[User]:
        return User.query().all()


    @classmethod
    def get_user_by_id(cls, id: int) -> Optional[User]:
        return User.find_by_id(id)
    

    @classmethod
    def create_user(cls, payload: UserCreate | dict) -> User:
        return User.create(payload)
    

    @classmethod
    def update_user(cls, id, payload: UserUpdate | dict) -> User | None:
        return User.update(id, payload)
    

    @classmethod
    def delete_user(cls, id) -> User | None:
        return User.delete_soft(id)

user_service = UserServiceImpl()