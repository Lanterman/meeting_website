import os
import jwt
import string
import secrets
import hashlib

from random import choice
from fastapi import BackgroundTasks

from config.utils import PATH_TO_USER_DIRECTORIES, ALGORITHM
from . import models, schemas


def create_random_salt(length=12) -> str:
    """Create random salt for password hashing"""

    query = "".join(choice(string.ascii_letters) for _ in range(length))
    return query


def password_hashing(password: str, salt: str = None) -> hex:
    """Password hashing with salt"""

    if salt is None:
        salt = create_random_salt()
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return enc.hex()


def validate_password(password: str, hashed_password: str) -> bool:
    """Check if password matches hashed password from database"""

    salt, hashed = hashed_password.split("$")
    return password_hashing(password, salt) == hashed


def create_user_directory(user_id) -> None:
    """Create user directory to save his photo"""

    if str(user_id) not in os.listdir(PATH_TO_USER_DIRECTORIES):
        os.mkdir(path=f"{PATH_TO_USER_DIRECTORIES}/{user_id}")


def remove_user_directory(user_id) -> None:
    """Remove user directory to save his photo"""

    if str(user_id) in os.listdir(PATH_TO_USER_DIRECTORIES):
        os.rmdir(f"{PATH_TO_USER_DIRECTORIES}/{user_id}")


async def get_user_by_email(email: str) -> models.Users:
    """Get user or none"""

    query = await models.Users.objects.get_or_none(email=email)
    return query


async def create_random_user_secret_key(user_id: int) -> hex:
    """Create random user secret"""

    query = secrets.token_hex()

    await delete_user_secret_key(user_id)
    await models.SecretKey.objects.create(secret_key=query, user=user_id)

    return query


async def get_user_token(token: str) -> models.Token:
    """Get user token"""

    query = await models.Token.objects.select_related("user").get_or_none(token=token)
    return query


async def delete_user_secret_key(user_id: int) -> None:
    """Delete user token"""

    await models.SecretKey.objects.delete(user=user_id)


async def delete_user_token(user_id: int) -> None:
    """Delete user token"""

    await models.Token.objects.delete(user=user_id)


async def create_user_token(user_id: int) -> models.Token:
    """Create user token"""

    await delete_user_token(user_id)

    _secret_key = await create_random_user_secret_key(user_id=user_id)
    _token = jwt.encode(payload={"user_id": user_id}, key=_secret_key, algorithm=ALGORITHM)
    query = await models.Token.objects.create(token=_token, user=user_id)
    return query


async def create_user(form_data: schemas.CreateUser, back_task: BackgroundTasks) -> dict:
    """Create user"""

    salt = create_random_salt()
    hashed_password = password_hashing(form_data.password, salt)
    form_data.password = f"{salt}${hashed_password}"
    query = await models.Users.objects.create(**form_data.dict())

    back_task.add_task(create_user_directory, query.id)

    token = await create_user_token(user_id=query.id)

    token_info = {"token": token.token, "expires": token.expires}

    return {**form_data.dict(), "token": token_info}


async def update_user_infor(form_data: schemas.UpdateUserInfo):
    """Update user information"""

    print(form_data)


async def delete_user(back_task: BackgroundTasks, user: models.Users) -> int:
    """Delete user"""

    back_task.add_task(remove_user_directory, user.id)

    query = await user.delete()
    return query
