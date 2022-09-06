from fastapi import APIRouter

from . import models

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.get("/")
async def get_users():
    users = await models.User.objects.all()
    return users
