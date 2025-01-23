from fastapi import APIRouter, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.Core.DB.database import get_db
from app.image_upload.services import handle_image_upload  
from app.utils.logging_config import configure_logger 

logger = configure_logger() 

router = APIRouter()

@router.post("/upload_image/")
async def upload_image(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)) :
    try:
        response = await handle_image_upload(file, db)

        return JSONResponse(
            content=response,
            status_code=200
        )

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JSONResponse(content={"message": "Failed to upload image", "error": str(e)}, status_code=500)
