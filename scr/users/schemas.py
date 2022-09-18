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


class UpdateUserInfo(BaseUser):
    """Update user information - schema"""

    @validator("gender")
    def is_gender_allowed(cls, value):
        """Check if gender is allowed"""

        if value not in models.GENDER:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=f"No such gender! Allowed list: {', '.join(models.GENDER)}")
        return value


class CreateUser(UpdateUserInfo):
    """Create user - schemas"""

    password: str


class ResetPassword(BaseModel):
    """Reset password - schema"""

    old_password: str
    new_password: str
    confirm_password: str

    @validator("new_password")
    def check_new_password_and_old_password_dont_match(cls, value, values):
        """Check if old password and don't match"""

        if value == values["old_password"]:
            raise HTTPException(detail="New password can not match old one!", status_code=status.HTTP_400_BAD_REQUEST)

        return value

    @validator("confirm_password")
    def check_passwords_match(cls, value, values):
        """Check if new password and confirmation password match"""

        if value != values["new_password"]:
            raise HTTPException(detail="Passwords do not match!", status_code=status.HTTP_400_BAD_REQUEST)

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
