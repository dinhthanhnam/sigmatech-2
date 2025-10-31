from fastapi import APIRouter
from schemas.product import ProductRead
from services.impl.product_service_impl import product_service
from typing import List, Union, Optional
from models.product import Product


router = APIRouter(prefix="/products", tags=["Products"])


def flatten(product: Optional[Product]):
    if not product:
        return None

    data = product.model_dump(exclude={"product_attribute"})
    # ép từng thuộc tính thành key: value
    for pa in product.product_attribute:
        # lấy tên attribute từ quan hệ attribute
        attr_name = getattr(pa.attribute, "name", None)
        if attr_name:
            data[attr_name] = pa.value

    return data


@router.get(path="",response_model=List[ProductRead])
def index():
    products = product_service.get_all_products()
    return [flatten(p) for p in products]


@router.get(path='/{product_id}',response_model=ProductRead)
def show(product_id: int):
    return flatten(product_service.get_product_by_id(product_id))


# @router.post("/", response_model=ProductRead)
# def store(payload: ProductCreate):
#     return product_service.create_product(payload)


# @router.patch('/{product_id}', response_model=ProductRead)
# def update(product_id: int, payload: ProductUpdate):
#     return product_service.update_product(product_id, payload)


# @router.delete('/{product_id}', response_model=ProductRead)
# def destroy(product_id: int):
#     return product_service.delete_product(product_id)