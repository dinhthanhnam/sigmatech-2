from fastapi import APIRouter
from models.user import UserRead
from services.impl.user_service_impl import user_service
from typing import List


router = APIRouter(prefix="/users", tags=["Users"])


@router.get(path='/',response_model=List[UserRead])
def index():
    return user_service.get_all_user()