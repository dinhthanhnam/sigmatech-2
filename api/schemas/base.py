from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime


class BaseSchema(SQLModel, table=False):
    pass


class BaseReadSchema(BaseSchema):
    created_at: Optional[datetime] = None


class BaseUpdateSchema(BaseSchema):
    pass