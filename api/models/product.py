from sqlmodel import SQLModel, Field, Relationship, Index, Session
from typing import Optional, List, Type
from .base import Base
from .base import T
from fastapi import HTTPException

class Product(Base, table=True):
    __tablename__ = "products" # type: ignore
    __table_args__ = (
        Index("idx_product_name", "name"),
    )

    name: str

    product_attribute: List["ProductAttribute"] = Relationship(back_populates="product") # type: ignore


    #override
    @classmethod
    def query(cls: type[T], sess: Session | None = None):
        query = super().query(sess)
        query = query.with_("product_attribute")
        return query

    #override
    @classmethod
    def find_by_id(cls: type[T], id: int, sess: Session | None = None)-> Optional[T]:
        return cls.query(sess).where(cls.id == id).first()

    # @classmethod
    # def get_attr(cls):
    #     return

    #override
    @classmethod
    def create(cls: type[T], data: SQLModel | dict, sess: Session | None = None) -> T:
        raw = data.model_dump() if isinstance(data, SQLModel) else dict(data)


        product_payload = {"name": raw.get("name")}
        product = cls.query(sess).create(product_payload)

        attrs_payload = []
        from .attribute import Attribute as a
        from .product_attribute import ProductAttribute as pa

        for key, value in raw.items():
            if key == "name":
                continue
            # tìm attribute template (nếu đã tồn tại)
            attribute = a.query(sess).where(a.name == key).first()
            # Không tồn tại thì dừng
            if not attribute:
                return
            attribute_id = attribute.id

            attrs_payload.append({
                "product_id": product.id,
                "attribute_id": attribute_id,
                "value": value
            })

        if attrs_payload:
            pa.query(sess).create_many(attrs_payload)
        
        return product


