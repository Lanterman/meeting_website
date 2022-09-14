from fastapi import APIRouter, Depends, status

from config.dependecies import get_current_user
from . import schemas, models, services


main_router = APIRouter(tags=["main"])


@main_router.post("/set_search", response_model=schemas.BaseSearchOptions, status_code=status.HTTP_201_CREATED)
async def set_search_parameters(form_data: schemas.CreateSearch, current_user: models.Users = Depends(get_current_user)):
    """Set search parameters for search users"""

    search_parameters = await services.create_search_parameters(data=form_data, user_id=current_user.id)
    return search_parameters
