import os
from sqlalchemy.ext.asyncio import AsyncSession
from app.image_upload import models
from app.utils.file_utils import generate_uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from datetime import datetime
from fastapi import HTTPException, UploadFile 
async def save_image_metadata(file_location: str, file: UploadFile, db: AsyncSession):
    """
    Saves image metadata to the database, including its UUID, filename, size, extension, path, and timestamps.
    :param file_location: The location where the file is saved
    :param file: The uploaded file
    :param db: The database session
    :return: The saved image metadata object
    """
    try:
        # Create a new image record in the database
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

async def get_image_path_from_db(image_id: int, db: AsyncSession) -> str:
    """
    Fetches the file path of an image from the database using its ID.
    :param image_id: The ID of the image to fetch
    :param db: The database session
    :return: The file path of the image
    """
    try:
        # Query to get the image path by image_id
        query = select(models.Image).where(models.Image.id == image_id)
        result = await db.execute(query)

        image = result.scalars().first()

        if not image:
            raise HTTPException(status_code=404, detail="Image not found")

        return image.path  # Return the image file path

    except Exception as e:
        raise Exception(f"Error while fetching image from database: {str(e)}")
