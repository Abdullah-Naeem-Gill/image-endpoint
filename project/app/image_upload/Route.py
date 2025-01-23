from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse, JSONResponse
from fastapi import File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.Core.DB.database import get_db
from app.image_upload.services import handle_image_upload, download_image  # <-- Make sure download_image is imported correctly
from app.utils.logging_config import configure_logger

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
async def download_image_route(image_id: int, db: AsyncSession = Depends(get_db)):
    try:
        # Call the download_image service function
        return await download_image(image_id, db)
    except Exception as e:
        logger.error(f"Error in downloading image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error downloading image: {str(e)}")
