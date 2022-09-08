import ormar

from pathlib import Path

from .db import metadata, database


# JWT settings
SECRET = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

BASE_DIR = Path(__file__).resolve().parent.parent
PATH_TO_USER_DIRECTORIES = f"{BASE_DIR}/uploaded_photo"


class MainMeta(ormar.ModelMeta):
    metadata = metadata
    database = database

