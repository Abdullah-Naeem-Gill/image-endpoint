from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid
from uuid import UUID
from sqlalchemy import func
from sqlalchemy import DateTime
from pydantic import BaseModel

class ImageBase(SQLModel):
    """ Base model for image metadata """
    uuid: UUID
    name: str
    size: int
    extension: str
    path: str

    class Config:
        """ Configuration for the ImageBase model """
        json_schema_extra = {
            "example": {
                "uuid": "f9c9746a-6e2e-4a78-b6f1-45e7c4216a4d",
                "name": "image1.png",
                "size": 12345,
                "extension": ".png",
                "path": "/images/image1.png",
            }
        }

class Image(ImageBase, table=True):
    """ Represents an image saved in the database with additional fields like id and timestamps """
    __tablename__ = "image"

    id: Optional[int] = Field(default=None, primary_key=True)  # Primary Key field
    uuid: UUID = Field(default_factory=uuid.uuid4, index=True)  # Auto-generated UUID
    created_at: datetime = Field(
        default=None,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={'server_default': func.now()},  # Automatically sets the timestamp on insert
    )
    updated_at: datetime = Field(
        default=None,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={
            'onupdate': func.now(),  # Automatically updates on every update
            'server_default': func.now(),  # Set the default value when the record is created
        },
    )

    class Config:
        """ Configuration for the Image model """
        orm_mode = True  # Makes SQLAlchemy models compatible with Pydantic models for FastAPI responses
        json_schema_extra = {
            "example": {
                "id": 1,
                "uuid": "f9c9746a-6e2e-4a78-b6f1-45e7c4216a4d",
                "name": "image1.png",
                "size": 12345,
                "extension": ".png",
                "path": "/images/image1.png",
                "created_at": "2025-01-23T00:00:00",
                "updated_at": "2025-01-23T00:00:00"
            }
        }

class ImageResponse(BaseModel):
    """ Pydantic model for image metadata response """
    id: int
    uuid: UUID
    name: str
    size: int
    extension: str
    path: str
    created_at: datetime
    updated_at: datetime

    class Config:
        """ Configuration for the ImageResponse model """
        orm_mode = True  # Ensures that SQLAlchemy models are converted to Pydantic models
        json_schema_extra = {
            "example": {
                "id": 1,
                "uuid": "f9c9746a-6e2e-4a78-b6f1-45e7c4216a4d",
                "name": "image1.png",
                "size": 12345,
                "extension": ".png",
                "path": "/images/image1.png",
                "created_at": "2025-01-23T00:00:00",
                "updated_at": "2025-01-23T00:00:00"
            }
        }

