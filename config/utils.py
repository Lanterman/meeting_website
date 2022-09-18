import ormar

from pathlib import Path

from .db import metadata, database


# JWT settings
ALGORITHM = "HS256"

BASE_DIR = Path(__file__).resolve().parent.parent
PATH_TO_USER_DIRECTORIES = f"{BASE_DIR}/uploaded_photo"

GENDER = ["Man", "Girl"]
SEARCH_BY_GENDER = ["Man", "Girl", "Both"]

EXTENSION_TYPES = ["image/jpeg", "image/bmp", "image/png", "image/jpg", "image/gif"]


class MainMeta(ormar.ModelMeta):
    metadata = metadata
    database = database

