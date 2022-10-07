import pytest

from httpx import AsyncClient

from config.utils import DOMAIN as url
from main import app
from test.test_data import search_parameters_for_girl, token


@pytest.mark.asyncio
async def test_set_search_parameters():
    async with AsyncClient(app=app, base_url=url) as ac:
        response = await ac.post("/set_search", json=search_parameters_for_girl, headers={"Authorization": token.value})

    data = response.json()
    assert response.status_code == 201, response.text
    assert data['search_by_gender'] == 'Girl', response.text


