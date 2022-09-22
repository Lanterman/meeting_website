from pydantic import EmailStr
from ormar import exceptions

from config.utils import user_validation_check
from . import models, schemas
from scr.users import services as user_services


async def update_or_create_search_parameters(data: schemas.CreateSearch, user_id: int):
    """Create search parameters for search users"""

    try:
        query = await models.SearchOptions.objects.update_or_create(id=user_id, **data.dict(), user=user_id)
    except exceptions.NoMatch:
        query = await models.SearchOptions.objects.create(id=user_id, **data.dict(), user=user_id)
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

    await user_validation_check(user, current_user, msg="You can not remove likes from yourself!")

    await models.Like.objects.delete(owner=current_user, like=user)


async def set_like(user_email: EmailStr, current_user: models.Users) -> models.Like:
    """Set like for user"""

    user = await user_services.get_user_by_email(user_email)

    await user_validation_check(user, current_user, msg="You can not like yourself!")

    await delete_like(user, current_user)

    query = await models.Like.objects.create(owner=current_user, like=user)
    return query


async def remove_from_favorites(user: models.Users, current_user: models.Users) -> None:
    """Remove from favorites"""

    await user_validation_check(user, current_user, msg="You can not remove yourself from your favorites!")

    await models.Favorite.objects.delete(owner=current_user, favorite=user)


async def add_to_favorites(user_email: EmailStr, current_user: models.Users) -> models.Favorite:
    """Add user to favorites"""

    user = await user_services.get_user_by_email(user_email)

    await user_validation_check(user, current_user, msg="You can not add yourself to favorites!")

    await remove_from_favorites(user, current_user)

    query = await models.Favorite.objects.create(owner=current_user, favorite=user)
    return query


async def get_chat(chat_id: int):
    """Get users chat"""

    query = await models.Chat.objects.prefetch_related(["users", "chat_messages", "chat_messages__owner"]).get_or_none(
        id=chat_id)
    return query


async def create_chat(user, current_user) -> models.Chat:
    """Create chat with user"""

    query = await models.Chat.objects.create()
    await query.users.add(user)
    await query.users.add(current_user)
    return query


async def chat(chat_id: int, user_email: EmailStr, current_user: models.Users):
    """Chat with user"""

    user = await user_services.get_user_by_email(user_email)
    await user_validation_check(user, current_user, msg="You can not create chat with yourself!")
    query = await get_chat(chat_id)

    if not query:
        query = await create_chat(user, current_user)

    return query


async def create_message(chat_id: int, message: str, current_user: models.Users) -> models.Message:
    """Send message to chat"""

    _chat = await get_chat(chat_id)
    query = await models.Message.objects.create(message=message, chat=_chat, owner=current_user)
    return query
