import os
import logging
from pathlib import Path
from fastapi import HTTPException, UploadFile, APIRouter, Depends, status
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.file_utils import allowed_file, create_date_folder, generate_uuid, save_file
from app.image_upload.db_crud import save_image_metadata, get_image_path_from_db
from app.image_upload.models import ImageResponse
from app.utils.logging_config import configure_logger
from fastapi.responses import FileResponse
logger = configure_logger()

ALLOWED_EXTENSIONS = os.getenv("ALLOWED_IMAGE_EXTENSIONS", "jpg,png").split(',')
BASE_DIR = Path(__file__).resolve().parent.parent.parent / "Data"
BASE_DIR.mkdir(parents=True, exist_ok=True)

router = APIRouter()

async def handle_image_upload(file: UploadFile, db: AsyncSession) -> ImageResponse:
    try:
        if not allowed_file(file.filename, ALLOWED_EXTENSIONS):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file extension. Allowed extensions are: {', '.join(ALLOWED_EXTENSIONS)}"
            )

        unique_filename = generate_uuid() + "." + file.filename.split('.')[-1]
        logger.info(f"Generated unique filename: {unique_filename}")

        date_folder = create_date_folder(BASE_DIR)
        logger.info(f"Created folder: {date_folder}")

        file_location = date_folder / unique_filename
        logger.info(f"Saving file to: {file_location}")

        await save_file(file, file_location)
        logger.info(f"File saved successfully: {file_location}")

        image_metadata = await save_image_metadata(file_location, file, db)
        logger.info(f"Image metadata saved to DB: {image_metadata}")

        if isinstance(image_metadata, ImageResponse):
            return image_metadata
        else:
            return ImageResponse.model_validate(image_metadata)

    except HTTPException as e:
        logger.error(f"HTTP error: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")

async def download_image(image_uuid: UUID, db: AsyncSession) -> FileResponse:
    try:
        image_metadata = await get_image_path_from_db(image_uuid, db)
        logger.info(f"Retrieved image metadata: {image_metadata}")

        image_path = Path(image_metadata['path']).resolve()
        logger.info(f"Normalized image path: {image_path}")

        if not image_path.exists():
            logger.error(f"Image file not found at path: {image_path}")
            raise HTTPException(status_code=404, detail="Image file not found on server")

        return FileResponse(image_path, media_type="application/octet-stream", filename=image_metadata['name'])

    except Exception as e:
        logger.error(f"Error in downloading image with UUID {image_uuid}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error downloading image: {str(e)}")