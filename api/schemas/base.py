from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime


class BaseSchema(SQLModel, table=False):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None