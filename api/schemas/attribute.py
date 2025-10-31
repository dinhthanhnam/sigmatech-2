from typing import Optional
from .base import SQLModel
from typing import Literal


class BaseAttribute(SQLModel, table=False):
    name: str
    model: str


class LaptopAttribute(BaseAttribute):
    lap_size: str
    mon_size: str
    type: Literal["laptop"] = "laptop"


class MonitorAttribute(BaseAttribute):
    mon_size: str
    type: Literal["monitor"] = "monitor"