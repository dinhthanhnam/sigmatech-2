from abc import ABC, abstractmethod


class PostService(ABC):
    
    @classmethod
    @abstractmethod
    def get_all_posts(cls):
        pass
    
    @classmethod
    @abstractmethod
    def get_post_by_id(cls):
        pass