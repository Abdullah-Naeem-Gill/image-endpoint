from sqlalchemy.ext.asyncio import AsyncSession
from app import models
from datetime import datetime
import os
from fastapi import UploadFile  # <-- Add this import
from app.utils.file_utils import generate_uuid

async def save_image_metadata(file_location: str, file: UploadFile, db: AsyncSession):

    try:
        image_metadata = models.Image(
            uuid=generate_uuid(),
            name=file.filename,
            size=os.path.getsize(file_location),
            extension=file.filename.split('.')[-1],
            path=str(file_location),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        db.add(image_metadata)
        await db.commit()
        await db.refresh(image_metadata)

        return image_metadata
    except Exception as e:
        raise Exception(f"Error while saving image metadata: {str(e)}")
