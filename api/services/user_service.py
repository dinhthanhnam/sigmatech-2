from abc import ABC, abstractmethod


class UserService(ABC):
    
    
    @classmethod
    @abstractmethod
    def get_all_user(cls):
        pass
    