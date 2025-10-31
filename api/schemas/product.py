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


ProductRead = Annotated[Union[LaptopRead, MonitorRead], Body(discriminator="type")]
ProductCreate = Annotated[Union[LaptopCreate, MonitorCreate], Body(discriminator="type")]