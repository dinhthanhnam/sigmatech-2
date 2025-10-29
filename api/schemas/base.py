from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BaseSchema(BaseModel):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None