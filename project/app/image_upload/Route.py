from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse, JSONResponse
from fastapi import File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.Core.DB.database import get_db
from app.image_upload.services import handle_image_upload
from app.utils.logging_config import configure_logger
import os
from pathlib import Path
from sqlalchemy.sql import text

logger = configure_logger()

router = APIRouter()

@router.post("/upload_image/")
async def upload_image(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    try:
        response = await handle_image_upload(file, db)

        return JSONResponse(
            content=response,
            status_code=200
        )

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JSONResponse(content={"message": "Failed to upload image", "error": str(e)}, status_code=500)

@router.get("/download_image/{image_id}")
async def download_image(image_id: int, db: AsyncSession = Depends(get_db)):
    try:
        # Query the database to get the image file's path based on image_id
        query = text("SELECT path FROM image WHERE id = :image_id")
        result = await db.execute(query, {'image_id': image_id})
        image = result.fetchone()

        if not image:
            raise HTTPException(status_code=404, detail="Image not found")

        image_path = image[0]  # The file path of the image
        logger.info(f"Retrieved image path: {image_path}")

        # Normalize the path
        image_path = Path(image_path).resolve()  # Resolve the absolute path
        logger.info(f"Normalized image path: {image_path}")

        # Check if file exists at the given path
        if not image_path.exists():
            logger.error(f"Image file not found at path: {image_path}")
            raise HTTPException(status_code=404, detail="Image file not found on server")

        # Return the file as a downloadable response
        return FileResponse(image_path, media_type='image/jpeg', filename=image_path.name)

    except Exception as e:
        logger.error(f"Error in downloading image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error downloading image: {str(e)}")
