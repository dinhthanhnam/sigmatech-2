from typing import Optional, Union, Annotated, Literal
from .user import UserRead
from .base import BaseSchema, BaseReadSchema, BaseUpdateSchema
from fastapi import Body


class BaseAttribute(BaseSchema):
    name: str
    model: str


class ProductBaseRead(BaseReadSchema):
    id: int


class ProductBaseUpdate(BaseUpdateSchema):
    name: Optional[str] = None
    model: Optional[str] = None


class LaptopAttribute(BaseAttribute):
    lap_size: str
    mon_size: str
    type: Literal["laptop"] = "laptop"


class MonitorAttribute(BaseAttribute):
    mon_size: str
    type: Literal["monitor"] = "monitor"


class LaptopRead(ProductBaseRead, LaptopAttribute):
    pass


class MonitorRead(ProductBaseRead, MonitorAttribute):
    pass


class LaptopCreate(LaptopAttribute):
    type: Literal["laptop"] = "laptop"
    pass


class MonitorCreate(MonitorAttribute):
    type: Literal["monitor"] = "monitor"
    pass


class LaptopUpdate(ProductBaseUpdate):
    lap_size: Optional[str] = None
    mon_size: Optional[str] = None
    type: Literal["laptop"] = "laptop"


class MonitorUpdate(ProductBaseUpdate):
    mon_size: Optional[str] = None
    type: Literal["monitor"] = "monitor"


ProductRead = Annotated[Union[LaptopRead, MonitorRead], Body(discriminator="type")]
ProductCreate = Annotated[Union[LaptopCreate, MonitorCreate], Body(discriminator="type")]
ProductUpdate = Annotated[Union[LaptopUpdate, MonitorUpdate], Body(discriminator="type")]