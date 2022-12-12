import pytest

from httpx import AsyncClient

from main import app
from apps.users import models as user_models
from apps.main import models as main_models
from test.test_data import token, user_url as url, updated_user_info, incorrect_user_info, password_reset_data, \
    invalid_password_reset_data


@pytest.mark.asyncio
async def test_profile():
    async with AsyncClient(app=app, base_url=url) as ac:
        request = await ac.get("/profile", headers={"Authorization": token.value})
        incorrect_request = await ac.get("/profile", headers={"Authorization": f"{token.value}123"})

    assert request.status_code == 200, request.text
    assert incorrect_request.status_code == 401, incorrect_request.text
    assert request.json()["first_name"] == "String"
    assert incorrect_request.json()["detail"] == "Invalid authentication credentials"


@pytest.mark.asyncio
async def test_update_info():
    async with AsyncClient(app=app, base_url=url) as ac:
        request = await ac.put("/update_info", headers={"Authorization": token.value}, json=updated_user_info)
        incorrect_request = await ac.put("/update_info", headers={"Authorization": token.value},
                                         json=incorrect_user_info)
        incorrect_request_with_token = await ac.put("/update_info", headers={"Authorization": f"{token.value}123"},
                                                    json=updated_user_info)

    assert request.status_code == 202, request.text
    assert incorrect_request.status_code == 406, incorrect_request.text
    assert incorrect_request_with_token.status_code == 401, incorrect_request_with_token.text
    assert request.json()["first_name"] == "Test"
    assert incorrect_request.json()["detail"] == "Min length email is 5 character!"
    assert incorrect_request_with_token.json()["detail"] == "Invalid authentication credentials"


@pytest.mark.asyncio
async def test_reset_password():
    async with AsyncClient(app=app, base_url=url) as ac:
        request = await ac.put("/reset_password", headers={"Authorization": token.value}, json=password_reset_data)
        incorrect_request_1 = await ac.put("/reset_password", headers={"Authorization": token.value},
                                           json=password_reset_data)
        incorrect_request_2 = await ac.put("/reset_password", headers={"Authorization": token.value},
                                           json=invalid_password_reset_data)

    assert request.status_code == 202, request.text
    assert incorrect_request_1.status_code == 400, incorrect_request_1.text
    assert incorrect_request_2.status_code == 400, incorrect_request_2.text
    assert request.json()["detail"] == "Successful!"
    assert incorrect_request_1.json()["detail"] == "Wrong old password!"
    assert incorrect_request_2.json()["detail"] == "Passwords do not match!"


@pytest.mark.asyncio
async def test_delete_db():
    """Clean DB after tests"""

    await user_models.Users.objects.delete(each=True)
    await main_models.Chat.objects.delete(each=True)
