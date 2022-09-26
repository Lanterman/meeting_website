from fastapi import APIRouter, Depends, status, Form
from pydantic import EmailStr

from config.dependecies import get_current_user
from . import schemas, models, services
from scr.users import services as user_services


main_router = APIRouter(tags=["main"])


@main_router.get("/search", response_model=list[schemas.SearchUser])
async def get_users_mathing_search(current_user: models.Users = Depends(get_current_user)):
    """Get users mathing search parameters"""

    users = await services.get_users(current_user)
    return users


@main_router.post("/set_search", response_model=schemas.BaseSearchOptions, status_code=status.HTTP_201_CREATED)
async def set_search_parameters(
        form_data: schemas.CreateSearch, current_user: models.Users = Depends(get_current_user)
):
    """Create or update search parameters for search users - endpoint"""

    search_parameters = await services.update_or_create_search_parameters(data=form_data, user_id=current_user.id)
    return search_parameters


@main_router.get("/{user_email}/set_like", response_model=schemas.BaseLike)
async def set_like(user_email: EmailStr, current_user: models.Users = Depends(get_current_user)):
    """Set like for user - endpoint"""

    _set_like = await services.set_like(user_email, current_user)
    return _set_like


@main_router.delete("/{user_email}/delete_like")
async def delete_like(user_email: EmailStr, current_user: models.Users = Depends(get_current_user)):
    """Delete like for user - endpoint"""

    user = await user_services.get_user_by_email(user_email)

    await services.delete_like(user, current_user)
    return {"detail": "successful!"}


@main_router.get("/{user_email}/add_to_favorites", response_model=schemas.BaseFavorite)
async def add_to_favorites(user_email: EmailStr, current_user: models.Users = Depends(get_current_user)):
    """Add user to favorites - endpoint"""

    favorites = await services.add_to_favorites(user_email, current_user)
    return favorites


@main_router.delete("/{user_email}/remove_from_favorites")
async def remove_from_favorites(user_email: EmailStr, current_user: models.Users = Depends(get_current_user)):
    """Remove from favorites - endpoint"""

    user = await user_services.get_user_by_email(user_email)

    await services.remove_from_favorites(user, current_user)
    return {"detail": "Successful!"}


@main_router.get("/chat/{chat_id}", response_model=schemas.Chat)
async def chat(chat_id: int, user_email: EmailStr, current_user: models.Users = Depends(get_current_user)):
    """Chat with user - endpoint"""

    _chat = await services.chat(chat_id, user_email, current_user)
    return _chat


@main_router.post("/chat/{chat_id}/send_msg", response_model=schemas.Message, status_code=status.HTTP_201_CREATED)
async def send_message(chat_id: int, message: str = Form(), current_user: models.Users = Depends(get_current_user)):
    """Send message to chat - endpoint"""

    message = await services.create_message(chat_id, message, current_user)
    return message
