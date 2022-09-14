from . import models, schemas


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
