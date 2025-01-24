
from fastapi import FastAPI, HTTPException
from app.image_upload.route import router as upload_router
from app.utils.logging_config import configure_logger
from app.Core.DB.database import initialize_db

logger = configure_logger()

async def lifespan(app: FastAPI):
    try:
        db_message = await initialize_db()  
        logger.info(db_message)
        yield
    except SQLAlchemyError as e:
        logger.error(f"Error initializing the database: {e}")
        raise HTTPException(status_code=500, detail="Error initializing the database")

app = FastAPI(lifespan=lifespan)

app.include_router(upload_router)
