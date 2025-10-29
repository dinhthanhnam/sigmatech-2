from fastapi import APIRouter
from schemas.post import PostRead
from services.impl.user_service_impl import user_service
from typing import List


router = APIRouter(prefix="/posts", tags=["posts"])


@router.get(path='/',response_model=List[PostRead])
def index():
    return user_service.get_all_user()