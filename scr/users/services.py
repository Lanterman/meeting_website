import datetime
import os

import aiofiles as aiofiles
import jwt
import string
import secrets
import hashlib
import uuid

from random import choice
from fastapi import BackgroundTasks, UploadFile, HTTPException, status

from config.utils import PATH_TO_USER_DIRECTORIES, ALGORITHM, EXTENSION_TYPES
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

    query = await models.Users.objects.get_or_none(email=email, is_activated=True)
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


async def update_user_info(form_data: schemas.UpdateUserInfo, user: models.Users) -> models.Users:
    """Update user information"""

    updated_user = await user.update(**form_data.dict(), update_date=datetime.datetime.now())
    return updated_user


async def reset_password(form_data: schemas.ResetPassword, user: models.Users) -> None:
    """Reset password"""

    salt = create_random_salt()
    hashed_password = password_hashing(form_data.new_password, salt)
    await user.update(password=f"{salt}${hashed_password}")


async def add_photo(file: UploadFile, user: models.Users) -> str:
    """Add photo to database and write to user directory"""

    content_type = file.content_type.split("/")[-1]
    path_to_photo = f"uploaded_photo/{user.id}/{uuid.uuid4()}.{content_type}"

    if file.content_type in EXTENSION_TYPES:
        async with aiofiles.open(path_to_photo, "wb") as buffer:
            data = await file.read()
            await buffer.write(data)
    else:
        raise HTTPException(
            detail="Unsupported content type! Must be jpeg, bmp, png, jpg or gif!",
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        )

    photo = await models.Photo.objects.create(path_to_photo=path_to_photo, user=user.id)
    return photo.path_to_photo


async def get_photo(photo_id: int):
    """Get photo"""

    query = await models.Photo.objects.get_or_none(id=photo_id)
    return query


async def delete_user(back_task: BackgroundTasks, user: models.Users) -> int:
    """Delete user"""

    back_task.add_task(remove_user_directory, user.id)

    query = await user.delete()
    return query


async def update_city(city: str, current_user: models.Users) -> models.Users:
    """update your city"""

    query = await current_user.update(city=city)
    return query
