import datetime

from pydantic import BaseModel, validator
from fastapi import HTTPException, status

from config.utils import SEARCH_BY_GENDER
from scr.users import models, schemas


class BaseSearchOptions(BaseModel):
    """Base search options"""

    search_by_gender: str
    search_by_age_to: int
    search_by_age_from: int


class BasePhoto(BaseModel):
    """Base photo - schema"""

    path_to_photo: str
    date_of_creation: datetime.datetime


class SearchUser(schemas.BaseUser):
    """Users mathing my search parameters"""

    photo_set: list[BasePhoto]


class CreateSearch(BaseSearchOptions):
    """Create search parameters"""

    @validator("search_by_gender")
    def is_gender_allowed(cls, value):
        """Check if gender is allowed"""

        if value not in SEARCH_BY_GENDER:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=f"No such gender! Allowed list: {', '.join(SEARCH_BY_GENDER)}")
        return value


class BaseLike(BaseModel):
    """Base like for user"""

    owner: schemas.BaseUser
    like: schemas.BaseUser
