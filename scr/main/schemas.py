import datetime

from pydantic import BaseModel, validator
from fastapi import HTTPException, status

from config import utils
from scr.users import schemas as user_schemas


class BasePhoto(BaseModel):
    """Base photo - schema"""

    path_to_photo: str
    date_of_creation: datetime.datetime


class UserWithPhoto(user_schemas.BaseUser):
    """User with photo - schema"""

    photo_set: list[BasePhoto]


class CreateSearch(utils.BaseSearchOptions):
    """Create search parameters - schema"""

    @validator("search_by_gender")
    def is_gender_allowed(cls, value):
        """Check if gender is allowed"""

        if value not in utils.settings.SEARCH_BY_GENDER:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=f"No such gender! Allowed list: {', '.join(utils.settings.SEARCH_BY_GENDER)}")
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
    """Base like for user - output schema"""

    owner: user_schemas.BaseUser
    like: user_schemas.BaseUser


class BaseFavorite(BaseModel):
    """Base favorite for user - output schema"""

    favorite: user_schemas.BaseUser


class Message(BaseModel):
    """User message - output schema"""

    message: str
    date_of_creation: datetime.datetime
    owner: user_schemas.BaseUser


class Chat(BaseModel):
    """Chat with user - schema"""

    users: list[user_schemas.BaseUser]
    chat_messages: list[Message]


class SearchUser(BaseModel):
    """Users mathing my search parameters - schema"""

    current_user: user_schemas.BaseUser
    found_users: list[UserWithPhoto]


class FavoritesList(BaseModel):
    """Users mathing my search parameters - schema"""

    current_user: user_schemas.BaseUser
    favorites: list[BaseFavorite]


class OutputSearchUser(utils.Notification, SearchUser):
    """Users mathing my search parameters - response schema"""


class OutputFavorite(utils.Notification, FavoritesList):
    """User favorites - response schema"""


class OutputChat(utils.Notification, Chat):
    """Output user chat - response schema"""
