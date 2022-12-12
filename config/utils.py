import os
import ormar
import logging

from typing import Any, Optional, Dict
from pathlib import Path
from fastapi import HTTPException, status
from fastapi_mail import ConnectionConfig
from pydantic import BaseModel, BaseSettings

from .db import metadata, database


# Path
BASE_DIR = Path(__file__).resolve().parent.parent
PATH_TO_USER_DIRECTORIES = f"{BASE_DIR}/uploaded_photo"

DOMAIN = os.environ.get("DOC_DOMAIN", os.environ["DOMAIN"])


conf = ConnectionConfig(
    MAIL_USERNAME=os.environ["MAIL_USERNAME"],
    MAIL_PASSWORD=os.environ["MAIL_PASSWORD"],
    MAIL_FROM=os.environ["MAIL_FROM"],
    MAIL_FROM_NAME=os.environ["MAIL_FROM_NAME"],
    MAIL_PORT=os.environ["MAIL_PORT"],
    MAIL_SERVER=os.environ["MAIL_SERVER"],
    MAIL_TLS=False,
    MAIL_SSL=True,
)


class LockedError(HTTPException):
    def __init__(self, status_code: int, detail: Any = None, headers: Optional[Dict[str, Any]] = None):
        logging.fatal(msg=detail)
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class Settings(BaseSettings):

    GENDER = ["Man", "Girl"]
    AGE = list(range(15, 81))
    SEARCH_BY_GENDER = ["Man", "Girl", "Both"]
    EXTENSION_TYPES = ["image/jpeg", "image/bmp", "image/png", "image/jpg", "image/gif"]


settings = Settings()


class MainMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class BaseSearchOptions(BaseModel):
    """Base search options - output schema"""

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
    """User validation check"""

    if not user:
        raise HTTPException(detail="Not found!", status_code=status.HTTP_404_NOT_FOUND)

    if user == current_user:
        raise HTTPException(detail=msg, status_code=status.HTTP_400_BAD_REQUEST)
