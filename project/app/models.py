from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Image(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: str
    name: str
    size: int
    extension: str
    path: str
    created_at: datetime
    updated_at: datetime
