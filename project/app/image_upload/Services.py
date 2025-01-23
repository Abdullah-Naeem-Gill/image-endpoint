import os
import logging
from pathlib import Path
from fastapi import HTTPException, UploadFile
from app.utils.file_utils import allowed_file, create_date_folder, generate_uuid, save_file
from app.image_upload.db_crud import save_image_metadata
from datetime import datetime

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = os.getenv("ALLOWED_IMAGE_EXTENSIONS", "jpg,png").split(',')
BASE_DIR = Path(__file__).resolve().parent.parent.parent / "Data"
BASE_DIR.mkdir(parents=True, exist_ok=True)

async def handle_image_upload(file: UploadFile, db) -> dict:
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

        image_dict = image_metadata.dict()

        return {
            "message": "Image uploaded successfully",
            "file_path": str(file_location),
            "metadata": image_dict
        }

    except HTTPException as e:
        logger.error(f"HTTP error: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")
