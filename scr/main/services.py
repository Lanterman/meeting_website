from fastapi import HTTPException, status
from pydantic import EmailStr

from . import models, schemas
from scr.users import services


async def delete_search_parameters(user_id: int) -> None:
    """Delete search parameters"""

    await models.SearchOptions.objects.delete(user=user_id)


async def create_search_parameters(data: schemas.CreateSearch, user_id: int):
    """Create search parameters for search users"""

    await delete_search_parameters(user_id)

    query = await models.SearchOptions.objects.create(**data.dict(), user=user_id)
    return query


async def get_search_parameters(user_id: int) -> models.SearchOptions:
    """Get search parameters"""

    query = await models.SearchOptions.objects.get_or_none(user=user_id)
    return query


async def get_users(user_id: int) -> list[models.Users]:
    """Get users mathing search parameters"""

    search_parameters = await get_search_parameters(user_id)
    age_range = range(search_parameters.search_by_age_to, search_parameters.search_by_age_from + 1)

    if search_parameters.search_by_gender == "Both":
        query = await models.Users.objects.select_related("photo_set").all(age__in=age_range)
    else:
        query = await models.Users.objects.select_related("photo_set").all(
            gender=search_parameters.search_by_gender, age__in=age_range
        )

    return query


async def delete_like(user: models.Users, current_user: models.Users) -> None:
    """Delete like for user"""

    if not user:
        raise HTTPException(detail="Not found!", status_code=status.HTTP_404_NOT_FOUND)

    if user == current_user:
        raise HTTPException(detail="You can not delete like yourself!", status_code=status.HTTP_400_BAD_REQUEST)

    await models.Like.objects.delete(owner=current_user, like=user)


async def set_like(user_email: EmailStr, current_user: models.Users):
    """Set like for user"""

    user = await services.get_user_by_email(user_email)

    if not user:
        raise HTTPException(detail="Not found!", status_code=status.HTTP_404_NOT_FOUND)

    if user == current_user:
        raise HTTPException(detail="You can not set like yourself!", status_code=status.HTTP_400_BAD_REQUEST)

    await delete_like(user, current_user)

    like = await models.Like.objects.create(owner=current_user, like=user)
    return like
