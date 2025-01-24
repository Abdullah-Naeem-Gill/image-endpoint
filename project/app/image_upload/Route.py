from fastapi import APIRouter, HTTPException, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.Core.DB.database import get_db
from app.image_upload.services import handle_image_upload
from app.utils.logging_config import configure_logger
from app.image_upload.models import ImageResponse
from fastapi.responses import FileResponse
from typing import Dict
from app.image_upload.services import download_image
from uuid import UUID
from fastapi import  status
logger = configure_logger()

router = APIRouter()

@router.post("/upload_image/", response_model=ImageResponse)
async def upload_image(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    """
    Uploads an image and returns the metadata.
    :param file: The image file uploaded
    :param db: Database session for saving metadata
    :return: A dictionary with a message and image metadata
    """
    try:
        image_metadata = await handle_image_upload(file, db)

        return image_metadata

    except Exception as e:
        logger.error(f"Unexpected error during image upload: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")

@router.get("/download_image/{image_uuid}", response_class=FileResponse)
async def download_image_route(image_uuid: UUID, db: AsyncSession = Depends(get_db)):
    try:
        return await download_image(image_uuid, db)
    except Exception as e:
        logger.error(f"Error in downloading image with UUID {image_uuid}: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Error downloading image: {str(e)}")