import ormar
import datetime

from pydantic import EmailStr

from config.utils import MainMeta, GENDER, AGE


class Users(ormar.Model):
    class Meta(MainMeta):
        tablename = "users"

    id: int = ormar.Integer(primary_key=True, index=True)
    first_name: str = ormar.String(max_length=50)
    last_name: str = ormar.String(max_length=50)
    email: EmailStr = ormar.String(max_length=50, unique=True, index=True)
    phone: str = ormar.String(max_length=20)
    gender: str = ormar.String(max_length=4, choices=GENDER, default="Man")
    age: int = ormar.Integer(minimum=15, maximum=80, choices=AGE)
    city: str = ormar.String(max_length=50)
    description: str = ormar.Text(nullable=True)
    password: str = ormar.String(max_length=500)
    is_activated: bool = ormar.Boolean(default=True)
    date_of_creation: datetime.datetime = ormar.DateTime(default=datetime.datetime.now())
    update_date: datetime.datetime = ormar.DateTime(default=datetime.datetime.now())


class SecretKey(ormar.Model):
    class Meta(MainMeta):
        tablename = "secret_key"

    id: int = ormar.Integer(primary_key=True, index=True)
    secret_key: str = ormar.String(max_length=300, unique=True)
    user: int = ormar.ForeignKey(to=Users, ondelete="CASCADE", related_name="secret_key_set")


class Token(ormar.Model):
    class Meta(MainMeta):
        tablename = "token"

    id: int = ormar.Integer(primary_key=True, index=True)
    token: str = ormar.String(max_length=300, index=True, unique=True)
    expires: datetime.datetime = ormar.DateTime(default=datetime.datetime.now() + datetime.timedelta(weeks=1))
    user: int = ormar.ForeignKey(to=Users, ondelete="CASCADE", related_name="token_set")


class Photo(ormar.Model):
    class Meta(MainMeta):
        tablename = "photo"

    id: int = ormar.Integer(primary_key=True, index=True)
    path_to_photo: str = ormar.String(max_length=100)
    date_of_creation: datetime.datetime = ormar.DateTime(default=datetime.datetime.now())
    user: int = ormar.ForeignKey(to=Users, ondelete="CASCADE", related_name="photo_set")
