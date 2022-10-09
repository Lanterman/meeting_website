import pytest

from httpx import AsyncClient

from config.utils import settings
from main import app
from test.test_data import search_parameters_for_girl, token, incorrect_search_parameters, main_url as url


@pytest.mark.asyncio
async def test_set_search_parameters():
    async with AsyncClient(app=app, base_url=url) as ac:
        request = await ac.post("/set_search", json=search_parameters_for_girl, headers={"Authorization": token.value})
        incorrect_request = await ac.post("/set_search", json=incorrect_search_parameters,
                                          headers={"Authorization": token.value})

    data = request.json()
    incorrect_data = incorrect_request.json()
    assert request.status_code == 201, request.text
    assert incorrect_request.status_code == 406, incorrect_request.text
    assert data["search_by_gender"] == "Girl", request.text
    assert incorrect_data["detail"] == f"No such gender! Allowed list: {', '.join(settings.SEARCH_BY_GENDER)}"


@pytest.mark.asyncio
async def test_get_users_mathing_search():
    async with AsyncClient(app=app, base_url=url) as ac:
        request = await ac.get("/search", headers={"Authorization": token.value})

    data = request.json()
    assert request.status_code == 200, request.text
    assert data["found_users"][0]["gender"] == "Girl", request.text


@pytest.mark.asyncio
async def test_set_like():
    async with AsyncClient(app=app, base_url=url) as ac:
        request = await ac.get("/2/set_like", headers={"Authorization": token.value})
        incorrect_request_1 = await ac.get("/1/set_like", headers={"Authorization": token.value})
        incorrect_request_2 = await ac.get("/3/set_like", headers={"Authorization": token.value})

    data = request.json()
    incorrect_data_1 = incorrect_request_1.json()
    incorrect_data_2 = incorrect_request_2.json()
    assert request.status_code == 200, request.text
    assert incorrect_request_1.status_code == 400, incorrect_request_1.text
    assert incorrect_request_2.status_code == 404, incorrect_request_2.text
    assert data["like"]["email"] == "test_user_girl@example.com", request.text
    assert incorrect_data_1["detail"] == "You can not like yourself!", incorrect_request_1.text
    assert incorrect_data_2["detail"] == "Not found!", incorrect_request_2.text


@pytest.mark.asyncio
async def test_delete_like():
    async with AsyncClient(app=app, base_url=url) as ac:
        request = await ac.delete("/2/delete_like", headers={"Authorization": token.value})
        incorrect_request_1 = await ac.delete("/1/delete_like", headers={"Authorization": token.value})
        incorrect_request_2 = await ac.delete("/3/delete_like", headers={"Authorization": token.value})

    data = request.json()
    incorrect_data_1 = incorrect_request_1.json()
    incorrect_data_2 = incorrect_request_2.json()
    assert request.status_code == 200, request.text
    assert incorrect_request_1.status_code == 400, incorrect_request_1.text
    assert incorrect_request_2.status_code == 404, incorrect_request_2.text
    assert data["detail"] == "Successful!", request.text
    assert incorrect_data_1["detail"] == "You can not remove likes from yourself!", incorrect_request_1.text
    assert incorrect_data_2["detail"] == "Not found!", incorrect_request_2.text


@pytest.mark.asyncio
async def test_add_to_favorites():
    async with AsyncClient(app=app, base_url=url) as ac:
        request = await ac.get("/2/add_to_favorites", headers={"Authorization": token.value})
        incorrect_request_1 = await ac.get("/1/add_to_favorites", headers={"Authorization": token.value})
        incorrect_request_2 = await ac.get("/3/add_to_favorites", headers={"Authorization": token.value})

    data = request.json()
    incorrect_data_1 = incorrect_request_1.json()
    incorrect_data_2 = incorrect_request_2.json()
    assert request.status_code == 200, request.text
    assert incorrect_request_1.status_code == 400, incorrect_request_1.text
    assert incorrect_request_2.status_code == 404, incorrect_request_2.text
    assert data["favorite"]["email"] == "test_user_girl@example.com", request.text
    assert incorrect_data_1["detail"] == "You can not add yourself to favorites!", incorrect_request_1.text
    assert incorrect_data_2["detail"] == "Not found!", incorrect_request_2.text


@pytest.mark.asyncio
async def test_get_favorites():
    async with AsyncClient(app=app, base_url=url) as ac:
        request = await ac.get("/favorites", headers={"Authorization": token.value})

    data = request.json()
    assert request.status_code == 200, request.text
    assert data["favorites"][0]["favorite"]["gender"] == "Girl", request.text


@pytest.mark.asyncio
async def test_remove_from_favorites():
    async with AsyncClient(app=app, base_url=url) as ac:
        request = await ac.delete("/2/remove_from_favorites", headers={"Authorization": token.value})
        incorrect_request_1 = await ac.delete("/1/remove_from_favorites", headers={"Authorization": token.value})
        incorrect_request_2 = await ac.delete("/3/remove_from_favorites", headers={"Authorization": token.value})

    data = request.json()
    incorrect_data_1 = incorrect_request_1.json()
    incorrect_data_2 = incorrect_request_2.json()
    assert request.status_code == 200, request.text
    assert incorrect_request_1.status_code == 400, incorrect_request_1.text
    assert incorrect_request_2.status_code == 404, incorrect_request_2.text
    assert data["detail"] == "Successful!", request.text
    assert incorrect_data_1["detail"] == "You can not remove yourself from your favorites!", incorrect_request_1.text
    assert incorrect_data_2["detail"] == "Not found!", incorrect_request_2.text


@pytest.mark.asyncio
async def test_create_chat():
    async with AsyncClient(app=app, base_url=url) as ac:
        request = await ac.get("/chat/2/create_chat", headers={"Authorization": token.value})
        incorrect_request_1 = await ac.get("/chat/1/create_chat", headers={"Authorization": token.value})
        incorrect_request_2 = await ac.get("/chat/3/create_chat", headers={"Authorization": token.value})

    assert request.status_code == 307, request.text
    assert incorrect_request_1.status_code == 400, incorrect_request_1.text
    assert incorrect_request_2.status_code == 404, incorrect_request_2.text


@pytest.mark.asyncio
async def test_chat():
    async with AsyncClient(app=app, base_url=url) as ac:
        request = await ac.get("/chat/1", headers={"Authorization": token.value})
        incorrect_request_1 = await ac.get("/chat/2", headers={"Authorization": token.value})

    data = request.json()
    incorrect_data_1 = incorrect_request_1.json()
    assert request.status_code == 200, request.text
    assert incorrect_request_1.status_code == 404, incorrect_request_1.text
    assert len(data["users"]) == 2, request.text
    assert data["users"][1]["gender"] == "Girl", request.text
    assert incorrect_data_1["detail"] == "Not found!", incorrect_data_1.text


@pytest.mark.asyncio
async def test_send_message():
    async with AsyncClient(app=app, base_url=url) as ac:
        request = await ac.post("/chat/1/send_msg", headers={"Authorization": token.value},
                                data={"message": "This is my test message!"})
        incorrect_request_1 = await ac.post("/chat/2/send_msg", headers={"Authorization": token.value},
                                            data={"message": "This is my test message!"})

    data = request.json()
    incorrect_data_1 = incorrect_request_1.json()
    assert request.status_code == 201, request.text
    assert incorrect_request_1.status_code == 400, incorrect_request_1.text
    assert data["message"] == "This is my test message!", request.text
    assert incorrect_data_1["detail"] == "No such chat!", incorrect_data_1.text
