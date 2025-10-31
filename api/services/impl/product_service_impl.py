from services.product_service import ProductService
from services import Product
from typing import Sequence, Optional
from schemas.product import ProductCreate


class ProductServiceImpl(ProductService):


    @classmethod
    def get_all_products(cls) -> Sequence[Product]:
        return Product.query().all()


    @classmethod
    def get_product_by_id(cls, id: int) -> Optional[Product]:
        return Product.find_by_id(id)
    

    # @classmethod
    # def create_product(cls, payload: ProductCreate | dict) -> Product:
    #     return Product.create(payload)
    

    # @classmethod
    # def update_Product(cls, id, payload: ProductUpdate | dict) -> Product | None:
    #     return Product.update(id, payload)
    

    @classmethod
    def delete_Product(cls, id) -> Product | None:
        return Product.delete_soft(id)

product_service = ProductServiceImpl()