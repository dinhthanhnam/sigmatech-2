from abc import ABC, abstractmethod


class UserService(ABC):
    
    @classmethod
    @abstractmethod
    def get_all_users(cls):
        pass

    @classmethod
    @abstractmethod
    def get_paginated_users(cls, page: int, take: int):
        pass

    @classmethod
    @abstractmethod
    def get_user_by_id(cls):
        pass

    @classmethod
    @abstractmethod
    def create_user(cls, payload):
        pass
    
    @classmethod
    @abstractmethod
    def update_user(cls, id, payload):
        pass

    @classmethod
    @abstractmethod
    def delete_user(cls, id):
        pass