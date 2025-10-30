from fastapi import APIRouter
from schemas.post import PostRead
from services.impl.post_service_impl import post_service
from typing import List


router = APIRouter(prefix="/posts", tags=["posts"])


@router.get(path='/',response_model=List[PostRead])
def index():
    return post_service.get_all_posts()


@router.post(path='/',response_model=List[PostRead])
def store():
    return post_service.get_all_posts()