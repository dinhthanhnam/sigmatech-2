from typing import Optional, Union, Annotated, Literal
from .user import UserRead
from .base import SQLModel
from .attribute import LaptopAttribute, MonitorAttribute
from fastapi import Body


class Product(SQLModel, table=False):
    id: int


class LaptopRead(Product, LaptopAttribute):
    pass


class MonitorRead(Product, MonitorAttribute):
    pass


class LaptopCreate(LaptopAttribute):
    pass


class MonitorCreate(MonitorAttribute):
    pass


class LaptopUpdate(LaptopAttribute):
    lap_size: Optional[str] = None
    mon_size: Optional[str] = None


class MonitorUpdate(MonitorAttribute):
    mon_size: Optional[str] = None


ProductRead = Annotated[Union[LaptopRead, MonitorRead], Body(discriminator="type")]
ProductCreate = Annotated[Union[LaptopCreate, MonitorCreate], Body(discriminator="type")]