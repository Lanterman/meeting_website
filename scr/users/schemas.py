import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


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


class CreateUser(BaseUser):
    """Create user - schemas"""

    password: str


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
