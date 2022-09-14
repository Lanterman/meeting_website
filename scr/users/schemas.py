import datetime

from typing import Optional
from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr, Field, validator

from . import models


class BaseUser(BaseModel):
    """Base User schema"""

    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    gender: str
    age: int
    city: str
    description: str


class SearchUser(BaseUser):
    """Users mathing my search parameters"""

    photo_set: list[models.Photo]


class CreateUser(BaseUser):
    """Create user - schemas"""

    password: str

    @validator("gender")
    def is_gender_allowed(cls, value):
        """Check if gender is allowed"""

        if value not in models.GENDER:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=f"No such gender! Allowed list: {', '.join(models.GENDER)}")
        return value


class BaseToken(BaseModel):
    """Base token schema"""

    token: str = Field(..., alias="access_token")
    expires: datetime.datetime
    type: Optional[str] = "Bearer"

    class Config:
        allow_population_by_field_name = True


class UserAndHisToken(BaseUser):
    """User information and hist token schema"""

    token: BaseToken = {}



