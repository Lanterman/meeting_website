import ormar
import datetime

from typing import ForwardRef
from pydantic import EmailStr
from pydantic.types import UUID4

from config.utils import MainMeta


GENDER = ["Man", "Girl"]
SEARCH_BY_GENDER = ["Man", "Girl", "Both"]

UserRef = ForwardRef("User")


class User(ormar.Model):
    class Meta(MainMeta):
        tablename = "user"

    id: int = ormar.Integer(primary_key=True, index=True)
    first_name: str = ormar.String(max_length=50)
    last_name: str = ormar.String(max_length=50)
    email: EmailStr = ormar.String(max_length=50, unique=True, index=True)
    phone: str = ormar.String(max_length=20)
    gender: str = ormar.String(max_length=4, choices=GENDER, default="Man")
    age: int = ormar.Integer(maximum=100)
    city: str = ormar.String(max_length=20)
    description: str = ormar.Text()
    hashed_password: str = ormar.String(max_length=500)
    is_activated: bool = ormar.Boolean(default=False)
    date_of_creation: datetime.datetime = ormar.DateTime(default=datetime.datetime.now())
    update_date: datetime.datetime = ormar.DateTime(default=datetime.datetime.now())
    favorites: UserRef = ormar.ManyToManyField(to=UserRef)

    search_by_gender: str = ormar.String(max_length=4, choices=SEARCH_BY_GENDER)
    search_by_age_to: int = ormar.Integer(default=10)
    search_by_age_from: int = ormar.Integer(default=20)


class Token(ormar.Model):
    class Meta(MainMeta):
        tablename = "token"

    id: int = ormar.Integer(primary_key=True, index=True)
    token: UUID4 = ormar.UUID(index=True, unique=True)
    date_of_creation: datetime.datetime = ormar.DateTime(default=datetime.datetime.now())
    user: int = ormar.ForeignKey(to=User, ondelete="CASCADE", related_name="token_set")


class Photo(ormar.Model):
    class Meta(MainMeta):
        tablename = "photo"

    id: int = ormar.Integer(primary_key=True, index=True)
    path_to_photo: str = ormar.String(max_length=100)
    date_of_creation: datetime.datetime = ormar.DateTime(default=datetime.datetime.now())
    user: int = ormar.ForeignKey(to=User, ondelete="CASCADE", related_name="photo_set")


class Like(ormar.Model):
    class Meta(MainMeta):
        tablename = "like"

    id: int = ormar.Integer(primary_key=True, index=True)
    owner: int = ormar.ForeignKey(to=User, ondelete="CASCADE", releted_name="like_set")
    like: int = ormar.ForeignKey(to=User, ondelete="CASCADE", related_name="dont_touch")


User.update_forward_refs()
