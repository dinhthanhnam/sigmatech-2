from sqlmodel import Field, Relationship, Index
from typing import Optional, List
from .base import Base


class Attribute(Base, table=True):
    __tablename__ = "attributes" # type: ignore
    __table_args__ = (
        Index("idx_attribute_name", "name"),
    )

    name: str

    product_attribute: List["ProductAttribute"] = Relationship(back_populates="attribute") # type: ignore
