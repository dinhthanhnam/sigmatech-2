from sqlmodel import Field, Relationship, Index
from typing import Optional, List
from .base import Base


class ProductAttribute(Base, table=True):
    __tablename__ = "product_attribute"  # type: ignore
    __table_args__ = (
        Index("idx_product_id", "product_id"),
        Index("idx_attribute_id", "attribute_id"),
        Index("uq_product_attr", "product_id", "attribute_id", unique=True),
    )

    product_id: int = Field(foreign_key="products.id", nullable=False)
    attribute_id: int = Field(foreign_key="attributes.id", nullable=False)
    value: Optional[str] = Field(default=None, index=True)

    product: Optional["Product"] = Relationship(back_populates="product_attribute")  # type: ignore
    attribute: Optional["Attribute"] = Relationship(back_populates="product_attribute") # type: ignore