import os
from sqlalchemy.ext.asyncio import AsyncSession
from app.image_upload import models
from app.utils.file_utils import generate_uuid
from sqlalchemy.future import select
from datetime import datetime
from fastapi import HTTPException, UploadFile
from uuid import UUID
from app.image_upload.models import Image  

async def save_image_metadata(file_location: str, file: UploadFile, db: AsyncSession) -> models.ImageResponse:
    """
    Saves image metadata to the database, including its UUID, filename, size, extension, path, and timestamps.
    :param file_location: The location where the file is saved
    :param file: The uploaded file
    :param db: The database session
    :return: The saved image metadata object
    """
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
   
async def get_image_path_from_db(image_uuid: UUID, db: AsyncSession) -> dict:
    try:
        query = select(Image).filter(Image.uuid == image_uuid)
        result = await db.execute(query)
        image_metadata = result.scalar_one_or_none()  

        if not image_metadata:
            raise HTTPException(status_code=404, detail="Image not found")

        return image_metadata.dict()  

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving image metadata: {str(e)}")