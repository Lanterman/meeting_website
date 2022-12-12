import random
import ormar

from fastapi import HTTPException, status
from ormar import exceptions

from config.utils import user_validation_check, settings
from . import models, schemas
from apps.users import services as user_services


def full_name(user: models.Users) -> str:
    """Create user full name"""

    query = user.first_name + " " + user.last_name
    return query


async def read_notification(notif_id: int) -> None:
    """Read user notification"""

    query = await models.Notification.objects.get(id=notif_id)
    await query.update(is_read=True)


async def search_users_by_city(city: str, user_id: int) -> list[models.Users] or []:
    """Search user by username"""

    query = await models.Users.objects.exclude(id=user_id).all(city=city.capitalize(), is_activated=True)
    return query


async def update_or_create_search_parameters(data: schemas.CreateSearch, user_id: int) -> models.SearchOptions:
    """Create search parameters for search users"""

    try:
        query = await models.SearchOptions.objects.update_or_create(id=user_id, **data.dict(), user=user_id)
    except exceptions.NoMatch:
        query = await models.SearchOptions.objects.create(id=user_id, **data.dict(), user=user_id)
    return query


async def get_search_parameters(user_id: int) -> models.SearchOptions or None:
    """Get search parameters"""

    query = await models.SearchOptions.objects.get_or_none(user=user_id)

    if query is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="To search for users, you must specify search parameters!"
        )

    return query


async def get_users(user) -> list[models.Users] or []:
    """Get users mathing search parameters"""

    search_parameters = await get_search_parameters(user.id)

    search_gender = search_parameters.search_by_gender

    query = await models.Users.objects.select_related("photo_set").exclude(id=user.id).all(
        ormar.and_(age__gte=search_parameters.search_by_age_to, age__lte=search_parameters.search_by_age_from),
        gender__in=[search_gender] if search_gender != "Both" else settings.GENDER,
        is_activated=True
    )

    random.shuffle(query)

    return query


async def create_notification(
        msg: str, first_user: models.Users, second_user: models.Users = None
) -> models.Notification:
    """Create notification"""

    if second_user:
        query = await models.Notification.objects.bulk_create(
            [
                models.Notification(notification=msg + full_name(second_user), user=first_user),
                models.Notification(notification=msg + full_name(first_user), user=second_user)
            ]
        )
    else:
        query = await models.Notification.objects.create(notification=msg, user=first_user)

    return query or second_user


async def get_unread_user_notifications(user_id: int) -> list[models.Notification] or []:
    """Get unread user notifications"""

    query = await models.Notification.objects.all(user__id=user_id, is_read=False)
    return query


async def get_like(owner: models.Users, like: models.Users) -> models.Like or None:
    """Get like"""

    query = await models.Like.objects.get_or_none(owner=owner, like=like)
    return query


async def delete_like(user: models.Users, current_user: models.Users) -> None:
    """Delete like for user"""

    await user_validation_check(user, current_user, msg="You can not remove likes from yourself!")

    await models.Like.objects.delete(owner=current_user, like=user)


async def check_reciprocity_like(
        receiving_user: models.Users, sending_user: models.Users
) -> models.Notification or None:
    """Check reciprocity like"""

    notification = None
    reciprocity_like = await get_like(owner=receiving_user, like=sending_user)

    if reciprocity_like:
        notification = await create_notification(
            msg="You have mutual like with ",
            first_user=sending_user,
            second_user=receiving_user
        )

    return notification


async def set_like(user_id: int, current_user: models.Users) -> tuple:
    """Set like for user"""

    user = await user_services.get_user_by_id(user_id)

    await user_validation_check(user, current_user, msg="You can not like yourself!")

    await delete_like(user, current_user)

    like = await models.Like.objects.create(owner=current_user, like=user)

    notification = await check_reciprocity_like(receiving_user=user, sending_user=current_user)

    return like, notification


async def remove_from_favorites(user: models.Users, current_user: models.Users) -> None:
    """Remove from favorites"""

    await user_validation_check(user, current_user, msg="You can not remove yourself from your favorites!")

    await models.Favorite.objects.delete(owner=current_user, favorite=user)


async def get_favorites(current_user: models.Users) -> list[models.Favorite] or []:
    """Get users favorites"""

    query = await models.Favorite.objects.select_related("favorite").all(owner=current_user)
    return query


async def add_to_favorites(user_id: int, current_user: models.Users) -> tuple:
    """Add user to favorites"""

    user = await user_services.get_user_by_id(user_id)

    await user_validation_check(user, current_user, msg="You can not add yourself to favorites!")

    await remove_from_favorites(user, current_user)

    notification = await create_notification(msg=f"{full_name(current_user)} add you to favorites!", first_user=user)

    query = await models.Favorite.objects.create(owner=current_user, favorite=user)
    return query, notification


async def get_chat_by_id(chat_id: int) -> models.Chat or None:
    """Get chat by chat id"""

    query = await models.Chat.objects.prefetch_related(["users", "chat_messages", "chat_messages__owner"]).get_or_none(
        id=chat_id)
    return query


async def get_chat_id(user_id: int, current_user_id: int) -> int or None:
    """Get users chat with id and email"""

    # query = await models.Chat.objects.select_related("users").get_or_none(
    #     ormar.and_(users__id=user_id), ormar.and_(users__id=current_user.id)
    # )

    query_1 = await models.Chat.objects.prefetch_related("users").all(ormar.and_(users__id=current_user_id))
    query_2 = await models.Chat.objects.prefetch_related("users").all(ormar.and_(users__id=user_id))
    _set_list = [_chat for _chat in query_1] + [_chat for _chat in query_2]
    query = [_chat for _chat in _set_list if _set_list.count(_chat) == 2]

    return query


async def create_chat(user_id: int, current_user: models.Users) -> int:
    """Create chat with user"""

    user = await user_services.get_user_by_id(user_id)
    await user_validation_check(user, current_user, msg="You can not create chat with yourself!")

    query = await get_chat_id(user_id, current_user.id)

    if not query:
        query = await models.Chat.objects.create()
        await query.users.add(user)
        await query.users.add(current_user)
    else:
        query = query[0]

    return query.id


async def chat(chat_id: int, current_user: models.Users) -> models.Chat:
    """Chat with user"""

    query = await get_chat_by_id(chat_id)

    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")

    if current_user not in query.users:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden!")

    return query


async def create_message(chat_id: int, message: str, current_user: models.Users) -> models.Message:
    """Send message to chat"""

    _chat = await get_chat_by_id(chat_id)

    if not _chat:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No such chat!")

    query = await models.Message.objects.create(message=message, chat=_chat, owner=current_user)
    return query
