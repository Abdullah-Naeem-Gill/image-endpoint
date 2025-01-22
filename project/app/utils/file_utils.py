import uuid
import os
from pathlib import Path
from datetime import datetime
import aiofiles
from fastapi import HTTPException

def allowed_file(filename: str, allowed_extensions: list) -> bool:
   
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def create_date_folder(base_dir: Path) -> Path:
   
    current_date = datetime.now().strftime('%Y-%m-%d')
    date_folder = base_dir / current_date
    date_folder.mkdir(parents=True, exist_ok=True)
    return date_folder

def generate_uuid() -> str:
   
    return str(uuid.uuid4())

async def save_file(file, file_location: Path):
   
    try:
        async with aiofiles.open(file_location, "wb") as f:
            await f.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {e}")
