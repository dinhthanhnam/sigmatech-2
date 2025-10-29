from abc import ABC, abstractmethod


class UserService(ABC):
    
    @classmethod
    @abstractmethod
    def get_all_user(cls):
        pass
    
    @classmethod
    @abstractmethod
    def get_user_by_id(cls):
        pass