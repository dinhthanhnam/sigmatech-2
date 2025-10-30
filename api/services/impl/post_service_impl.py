from services.post_service import PostService
from services import Post
from typing import Sequence, Optional
from schemas.post import PostCreate

class PostServiceImpl(PostService):

    
    @classmethod
    def get_all_posts(cls) -> Sequence[Post]:
        return Post.query().all()


    @classmethod
    def get_post_by_id(cls, id: int) -> Optional[Post]:
        return Post.find_by_id(id)
    

    @classmethod
    def create_user(cls, payload: PostCreate | dict) -> Post:
        return Post.create(payload)
    

post_service = PostServiceImpl()