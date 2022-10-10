import re
import string
import datetime

from typing import Optional
from fastapi import HTTPException, status, UploadFile
from pydantic import BaseModel, EmailStr, Field, validator

from config import utils


class BaseUser(BaseModel):
    """Base User - schema"""

    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    gender: str
    age: int
    city: str
    description: str
    is_activated: bool = False


class UpdateUserInfo(BaseUser):
    """Update user information - output schema"""

    @classmethod
    def check_first_character(cls, value) -> bool:
        """Check first character of field"""

        if value[0] not in string.ascii_letters:
            return False

        return True

    @classmethod
    def check_field(cls, field: str, field_name: str) -> str:
        """Check field"""

        if not UpdateUserInfo.check_first_character(field):
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=f"First character of '{field_name}' is unacceptable!"
            )

        return field

    @classmethod
    def capitalized_field(cls, field: str) -> str:
        """Write capitalized the field"""

        value = field.capitalize()
        return value

    @validator("first_name")
    def check_first_character_of_first_name(cls, value):
        """Check first character of first name"""

        return UpdateUserInfo.check_field(value, "First name")

    @validator("first_name")
    def capitalized_first_name(cls, value):
        """Write capitalized the first name"""

        return UpdateUserInfo.capitalized_field(value)

    @validator("last_name")
    def check_first_character_of_last_name(cls, value):
        """Check first character of last name"""

        return UpdateUserInfo.check_field(value, "Last name")

    @validator("last_name")
    def capitalized_last_name(cls, value):
        """Write capitalized the last name"""

        return UpdateUserInfo.capitalized_field(value)

    @validator("email")
    def check_first_character_of_email(cls, value):
        """Check first character of email"""

        return UpdateUserInfo.check_field(value, "Email")

    @validator("email")
    def check_email_length(cls, value):
        """Check email length"""

        string_before_dog = value.split("@")[0]

        if len(string_before_dog) < 5:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Min length email is 5 character!")

        return value

    @validator("phone")
    def check_phone_for_presence_plus(cls, value):
        """Check if phone number starts with +"""

        value = value if value[0] == "+" else "+" + value

        if not value[1:]:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Phone can not be empty!")

        return value

    @validator("phone")
    def check_characters(cls, value):
        """Check if phone number consists of only digits"""

        reg_list = re.findall("\D", value[1:])
        if reg_list or not value[1:]:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Phone must contain only numbers!")

        return value

    @validator("gender")
    def is_gender_allowed(cls, value):
        """Check if gender is allowed"""

        if value not in utils.settings.GENDER:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=f"No such gender! Allowed list: {', '.join(utils.settings.GENDER)}")
        return value

    @validator("age")
    def check_age(cls, value):
        """Check if age is more than 15 and less than 80"""

        if value not in utils.settings.AGE:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Age must be over 15 and under 80!")

        return value

    @validator("city")
    def capitalized_city(cls, value):
        """Write capitalized the city"""

        return UpdateUserInfo.capitalized_field(value)


class CreateUser(UpdateUserInfo):
    """Create user - output schema"""

    password: str

    @validator("password")
    def check_password_complexity(cls, value):
        """Check password complexity"""

        if len(value) < 10:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Password is too simple!")

        return value


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

    @validator("new_password")
    def check_password_complexity(cls, value):
        """Check password complexity"""

        return CreateUser.check_password_complexity(value)

    @validator("confirm_password")
    def check_passwords_match(cls, value, values):
        """Check if new password and confirmation password match"""

        if value != values["new_password"]:
            raise HTTPException(detail="Passwords do not match!", status_code=status.HTTP_400_BAD_REQUEST)

        return value


class AddPhoto(BaseModel):
    """Add photo - output schema"""

    path_to_photo: str
    photo: UploadFile


class BaseToken(BaseModel):
    """Base token - output schema"""

    token: str = Field(..., alias="access_token")
    expires: datetime.datetime
    type: Optional[str] = "Bearer"

    class Config:
        allow_population_by_field_name = True


class UserAndHisToken(BaseUser):
    """User information and hist token - output schema"""

    token: BaseToken = {}


class OutputProfile(utils.Notification, BaseUser):
    """Output profile - response schema"""

    is_activated: bool
    date_of_creation: datetime.datetime
    update_date: datetime.datetime
    search: utils.BaseSearchOptions
