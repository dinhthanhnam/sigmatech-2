from abc import ABC, abstractmethod


class ProductService(ABC):
    
    @classmethod
    @abstractmethod
    def get_all_products(cls):
        pass
    
    @classmethod
    @abstractmethod
    def get_product_by_id(cls):
        pass