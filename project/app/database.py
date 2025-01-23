
import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.utils.logging_config import logger  

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in environment variables")

engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db() -> AsyncSession:
 
    try:
        async with SessionLocal() as session:
            yield session
    except SQLAlchemyError as e:
        logger.error(f"Database connection error: {e}")
        raise HTTPException(status_code=500, detail="Database connection error")

async def init_db() -> None:
   
    try:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
    except SQLAlchemyError as e:
        logger.error(f"Error initializing the database: {e}")
        raise HTTPException(status_code=500, detail="Error initializing the database")
    else:
        logger.info("Database initialized successfully.")
