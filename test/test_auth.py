import pytest
from httpx import AsyncClient

from main import app
from test.test_data import user_info_1, user_info_2, incorrect_user_info, token, user_url as url


@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(app=app, base_url=url) as ac:
        request_1 = await ac.post("/sign-on", json=user_info_1)
        request_2 = await ac.post("/sign-on", json=user_info_2)
        duplicate_request = await ac.post("/sign-on", json=user_info_1)
        incorrect_request = await ac.post("/sign-on", json=incorrect_user_info)

    assert request_1.status_code == 201, request_1.text
    assert request_2.status_code == 201, request_2.text
    assert duplicate_request.status_code == 400, duplicate_request.text
    assert incorrect_request.status_code == 406, incorrect_request.text

    response_1 = request_1.json()
    response_2 = request_2.json()
    duplicate_request = duplicate_request.json()
    incorrect_response = incorrect_request.json()
    assert response_1["gender"] == "Man", request_1.text
    assert response_2["gender"] == "Girl", request_2.text
    assert duplicate_request["detail"] == "User with this email already exists!", duplicate_request.text
    assert incorrect_response["detail"] == "Min length email is 5 character!", incorrect_request.text


@pytest.mark.asyncio
async def test_auth():
    async with AsyncClient(app=app, base_url=url) as ac:
        correct_request = await ac.post("/auth", data={"username": "test_user@example.com", "password": "123412341234"})
        incorrect_request = await ac.post("/auth", data={"username": "test_user@example.com", "password": "1234123412"})

    assert correct_request.status_code == 202, correct_request.text
    assert incorrect_request.status_code == 400, incorrect_request.text

    response = correct_request.json()
    incorrect_response = incorrect_request.json()
    token.value = f"{response['type']} {response['access_token']}"
    assert response["type"] == "Bearer", correct_request.text
    assert incorrect_response["detail"] == "Incorrect email or password!"
