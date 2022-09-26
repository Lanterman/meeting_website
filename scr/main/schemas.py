import datetime

from pydantic import BaseModel, validator
from fastapi import HTTPException, status

from config.utils import SEARCH_BY_GENDER, BaseSearchOptions
from scr.users import schemas


class BasePhoto(BaseModel):
    """Base photo - schema"""

    path_to_photo: str
    date_of_creation: datetime.datetime


class SearchUser(schemas.BaseUser):
    """Users mathing my search parameters"""

    photo_set: list[BasePhoto]


class CreateSearch(BaseSearchOptions):
    """Create search parameters - schema"""

    @validator("search_by_gender")
    def is_gender_allowed(cls, value):
        """Check if gender is allowed"""

        if value not in SEARCH_BY_GENDER:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=f"No such gender! Allowed list: {', '.join(SEARCH_BY_GENDER)}")
        return value

    @validator("search_by_age_to")
    def age_must_be_greater_than_15(cls, value):
        """Check if age is greate than 15"""

        if value < 15:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Age to must be greate than 15!")
        return value

    @validator("search_by_age_from")
    def age_from_cannot_be_less_age_to(cls, value, values):
        """Check if age_from less age_to"""

        if value < values["search_by_age_to"]:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Age_to cannot be less that age_to!")
        return value

    @validator("search_by_age_from")
    def maximum_age(cls, value, values):
        """Check if age_from and age_to less 80"""

        if value > 80 or values["search_by_age_to"] > 80:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Age_to and age_to must be less 80!"
            )
        return value


class UpdateSearchData(CreateSearch):
    """Update search options - schema"""


class BaseLike(BaseModel):
    """Base like for user - schema"""

    owner: schemas.BaseUser
    like: schemas.BaseUser


class BaseFavorite(BaseModel):
    """Base favorite for user - schema"""

    owner: schemas.BaseUser
    favorite: schemas.BaseUser


class Message(BaseModel):
    """User message - schema"""

    message: str
    date_of_creation: datetime.datetime
    owner: schemas.BaseUser


class Chat(BaseModel):
    """Chat with user - schema"""

    users: list[schemas.BaseUser]
    chat_messages: list[Message]
