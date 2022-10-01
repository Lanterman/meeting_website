from fastapi import APIRouter, Depends, status, Form
from fastapi.responses import RedirectResponse

from config import utils
from config.dependecies import get_current_user
from . import schemas, models, services
from scr.users import services as user_services


main_router = APIRouter(tags=["main"])


@main_router.get("/search", response_model=schemas.OutputSearchUser)
async def get_users_mathing_search(current_user: models.Users = Depends(get_current_user)):
    """Get users mathing search parameters - response endpoint"""

    users = await services.get_users(current_user)
    return {"current_user": current_user, "found_users": users, "notification_set": current_user.notification_set}


@main_router.post("/set_search", response_model=utils.BaseSearchOptions, status_code=status.HTTP_201_CREATED)
async def set_search_parameters(
        form_data: schemas.CreateSearch, current_user: models.Users = Depends(get_current_user)
):
    """Create or update search parameters for search users - endpoint"""

    search_parameters = await services.update_or_create_search_parameters(data=form_data, user_id=current_user.id)
    return search_parameters


@main_router.get("/{user_id}/set_like", response_model=schemas.BaseLike)
async def set_like(user_id: int, current_user: models.Users = Depends(get_current_user)):
    """Set like for user - endpoint"""

    _set_like, notification = await services.set_like(user_id, current_user)

    if notification:
        pass

    return _set_like


@main_router.delete("/{user_id}/delete_like")
async def delete_like(user_id: int, current_user: models.Users = Depends(get_current_user)):
    """Delete like for user - endpoint"""

    user = await user_services.get_user_by_id(user_id)

    await services.delete_like(user, current_user)
    return {"detail": "successful!"}


@main_router.get("/favorites", response_model=schemas.OutputFavorite)
async def get_favorites(current_user: models.Users = Depends(get_current_user)):
    """Get user favorites - response endpoint"""

    favorites = await services.get_favorites(current_user)
    return {"current_user": current_user, "favorites": favorites, "notification_set": current_user.notification_set}


@main_router.get("/{user_id}/add_to_favorites", response_model=schemas.BaseFavorite)
async def add_to_favorites(user_id: int, current_user: models.Users = Depends(get_current_user)):
    """Add user to favorites - endpoint"""

    favorites, notifications = await services.add_to_favorites(user_id, current_user)

    if notifications:
        pass

    return favorites


@main_router.delete("/{user_id}/remove_from_favorites")
async def remove_from_favorites(user_id: int, current_user: models.Users = Depends(get_current_user)):
    """Remove from favorites - endpoint"""

    user = await user_services.get_user_by_id(user_id)

    await services.remove_from_favorites(user, current_user)
    return {"detail": "Successful!"}


@main_router.get("/chat/{chat_id}", response_model=schemas.OutputChat)
async def chat(chat_id: int, current_user: models.Users = Depends(get_current_user)):
    """Chat with user - response endpoint"""

    _chat = await services.chat(chat_id, current_user)

    return _chat.dict() | current_user.dict()


@main_router.get("/chat/{user_id}/create_chat")
async def create_chat(user_id: int, current_user: models.Users = Depends(get_current_user)):
    """Create chat and redirect to chat - endpoint"""

    chat_id = await services.create_chat(user_id, current_user)
    return RedirectResponse(url=f"{utils.DOMEN}/chat/{chat_id}/")


@main_router.post("/chat/{chat_id}/send_msg", response_model=schemas.Message, status_code=status.HTTP_201_CREATED)
async def send_message(chat_id: int, message: str = Form(), current_user: models.Users = Depends(get_current_user)):
    """Send message to chat - endpoint"""

    message = await services.create_message(chat_id, message, current_user)
    return message
