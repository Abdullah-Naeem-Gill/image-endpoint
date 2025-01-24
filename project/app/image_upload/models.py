from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid
from uuid import UUID
from sqlalchemy import func
from sqlalchemy import DateTime
from pydantic import BaseModel

class CommonConfig:
    json_schema_extra = {
        "example": {
            "uuid": "f9c9746a-6e2e-4a78-b6f1-45e7c4216a4d",
            "name": "image1.png",
            "size": 12345,
            "extension": ".png",
            "path": "/images/image1.png",
        }
    }

class ImageBase(SQLModel):
    """ Base model for image metadata with common fields """
    uuid: UUID
    name: str
    size: int
    extension: str
    path: str

    class Config(CommonConfig):
        pass

class Image(ImageBase, table=True):
    """ Represents an image saved in the database with uuid as the primary key and additional fields like timestamps """
    __tablename__ = "image"

    uuid: UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True) 
    created_at: datetime = Field(
        default=None,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={'server_default': func.now()},
    )
    updated_at: datetime = Field(
        default=None,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={
            'onupdate': func.now(),
            'server_default': func.now(),
        },
    )

    class Config(CommonConfig):
        from_attributes=True

class ImageResponse(BaseModel):
    """ Pydantic model for image metadata response """
    uuid: UUID
    name: str
    size: int
    extension: str
    path: str
    created_at: datetime
    updated_at: datetime

    class Config(CommonConfig):
        from_attributes=True 