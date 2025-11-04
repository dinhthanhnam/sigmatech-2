from abc import ABC, abstractmethod


class ProductService(ABC):
    
    @classmethod
    @abstractmethod
    def get_all_products(cls):
        pass
    
    @classmethod
    @abstractmethod
    def get_paginated_products(cls):
        pass

    @classmethod
    @abstractmethod
    def get_product_by_id(cls):
        pass

    @classmethod
    @abstractmethod
    def create_product(cls, payload):
        pass
    
    @classmethod
    @abstractmethod
    def update_product(cls, id, payload):
        pass

    @classmethod
    @abstractmethod
    def delete_product(cls, id):
        pass