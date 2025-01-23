import os
import logging
from pathlib import Path
from fastapi.responses import FileResponse
from fastapi import HTTPException, UploadFile
from app.utils.file_utils import allowed_file, create_date_folder, generate_uuid, save_file
from app.image_upload.db_crud import save_image_metadata, get_image_path_from_db
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

async def download_image(image_id: int, db) -> FileResponse:
    try:
        # Retrieve the image path from the database
        image_path = await get_image_path_from_db(image_id, db)
        logger.info(f"Retrieved image path: {image_path}")

        # Normalize the path
        image_path = Path(image_path).resolve()
        logger.info(f"Normalized image path: {image_path}")

        # Check if the image exists at the given path
        if not image_path.exists():
            logger.error(f"Image file not found at path: {image_path}")
            raise HTTPException(status_code=404, detail="Image file not found on server")

        # Return the file as a downloadable response
        return FileResponse(image_path, media_type='image/jpeg', filename=image_path.name)

    except Exception as e:
        logger.error(f"Error in downloading image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error downloading image: {str(e)}")
