from sqlalchemy.ext.asyncio import AsyncSession
from project.app.image_upload import models
from datetime import datetime
import os
from app.utils.file_utils import generate_uuid

async def save_image_metadata(file_location: str, file: UploadFile, db: AsyncSession):
    """
    Saves the image metadata to the database.

    :param file_location: The file's location on the server
    :param file: The uploaded file
    :param db: The database session
    :return: The saved image metadata
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
