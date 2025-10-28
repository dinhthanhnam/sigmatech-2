from services.user_service import UserService
from services import User
from typing import Sequence, Optional


class UserServiceImpl(UserService):

    
    @classmethod
    def get_all_user(cls) -> Sequence[User]:
        return User.find().all()


    @classmethod
    def get_user_by_id(cls, id: int) -> Optional[User]:
        return User.find_by_pk(id)
    

user_service = UserServiceImpl()