import ormar

from pathlib import Path

from fastapi import HTTPException, status
from pydantic import BaseModel

from .db import metadata, database


# JWT settings
ALGORITHM = "HS256"

BASE_DIR = Path(__file__).resolve().parent.parent
PATH_TO_USER_DIRECTORIES = f"{BASE_DIR}/uploaded_photo"

GENDER = ["Man", "Girl"]
AGE = list(range(15, 81))
SEARCH_BY_GENDER = ["Man", "Girl", "Both"]

EXTENSION_TYPES = ["image/jpeg", "image/bmp", "image/png", "image/jpg", "image/gif"]

DOMEN = "http://127.0.0.1:8000"


class MainMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class BaseSearchOptions(BaseModel):
    """Base search options"""

    search_by_gender: str
    search_by_age_to: int
    search_by_age_from: int


class BaseNotification(BaseModel):
    """Base user notification"""

    notification: str
    is_read: bool


class Notification(BaseModel):
    """Notification is for inheritance"""

    notification_set: list[BaseNotification] or []


async def user_validation_check(user, current_user, msg: str) -> None:
    """"""

    if not user:
        raise HTTPException(detail="Not found!", status_code=status.HTTP_404_NOT_FOUND)

    if user == current_user:
        raise HTTPException(detail=msg, status_code=status.HTTP_400_BAD_REQUEST)
