
# FastAPI Image Upload Project

This project is a simple FastAPI application that allows users to upload images to the server. The images are saved to a disk and their metadata is stored in a PostgreSQL database. It uses async functionality for both database interaction and file handling.

## Features

- Upload images with validation for allowed extensions.
- Save images to disk with a unique filename.
- Save image metadata (file size, path, etc.) to a PostgreSQL database.
- Asynchronous file handling using FastAPI and SQLAlchemy (async).
- Environment variables for database configuration and logging level.

## Requirements

- Python 3.7+
- PostgreSQL (or another compatible database)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Abdullah-Naeem-Gill/image-endpoint.git
cd your-repo-name

2. Set up a virtual environment
# Install virtualenv if you don't have it
pip install virtualenv

# Create a virtual environment
virtualenv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate


###3. Install dependencies

pip install -r requirements.txt


4. Set up environment variables


# Database configuration
DATABASE_URL=postgresql+asyncpg://username:password@localhost/dbname

# Logging level (optional, defaults to INFO)
LOGGING_LEVEL=INFO

# Allowed file extensions for image upload (optional)
ALLOWED_IMAGE_EXTENSIONS=jpg,png,jpeg


5. Create the database

If you haven't created the database already, you can manually create it in PostgreSQL, or the FastAPI application will create it automatically on the first run.

Make sure you have PostgreSQL installed and running

6. Running the application

uvicorn app.main:app --reload
