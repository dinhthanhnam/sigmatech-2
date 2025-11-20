from fastapi import APIRouter, HTTPException, Query
from schemas.product import ProductRead, ProductCreate
from services.impl.product_service_impl import product_service
from typing import List, Union, Optional
from models.product import Product
from i18n import t


router = APIRouter(prefix="/products", tags=["Products"])


def flatten(product: Product):
    data = product.model_dump(exclude={"product_attribute"})
    for pa in product.product_attribute:
        attr_name = getattr(pa.attribute, "name", None)
        if attr_name:
            data[attr_name] = pa.value

    return data


@router.get(path="",response_model=List[ProductRead])
def index(
        page: int = Query(1, ge=1)
    ):
    products = product_service.get_paginated_products(page=page, take=8)
    if not products:
        raise HTTPException(status_code=404, detail=t('common.product.not_found'))
    return [flatten(p) for p in products]


@router.get(path='/{product_id}',response_model=ProductRead)
def show(product_id: int):
    product = product_service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail=t('common.product.not_found'))
    return flatten(product)


@router.post("/", response_model=ProductRead)
def store(payload: ProductCreate):
    return product_service.create_product(payload)


# @router.patch('/{product_id}', response_model=ProductRead)
# def update(product_id: int, payload: ProductUpdate):
#     return product_service.update_product(product_id, payload)


# @router.delete('/{product_id}', response_model=ProductRead)
# def destroy(product_id: int):
#     return product_service.delete_product(product_id)