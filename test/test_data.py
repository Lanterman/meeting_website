import os
import ctypes

main_url = os.environ["DOMAIN"]
user_url = f"{main_url}/user"


token = ctypes.c_wchar_p(" ")

user_info_1 = {
    "first_name": "string", "last_name": "string", "email": "test_user@example.com", "phone": 2113111311111,
    "gender": "Man", "age": 22, "city": "string", "description": "string", "password": "123412341234"
}
user_info_2 = {
    "first_name": "string", "last_name": "string", "email": "test_user_girl@example.com", "phone": 2113111311111,
    "gender": "Girl", "age": 22, "city": "string", "description": "string", "password": "123412341234"
}
updated_user_info = {
    "first_name": "test", "last_name": "test", "email": "test_user1@example.com", "phone": 2113111311111,
    "gender": "Man", "age": 20, "city": "string", "description": "string", "password": "123412341234"
}
incorrect_user_info = {
    "first_name": "string", "last_name": "string", "email": "user@example.com", "phone": 2113111311111,
    "gender": "man", "age": 22, "city": "string", "description": "string", "password": "123412341234"
}

password_reset_data = {"old_password": "123412341234", "new_password": "12341234123", "confirm_password": "12341234123"}
invalid_password_reset_data = {
    "old_password": "123412341234", "new_password": "1234123412", "confirm_password": "12341234123"
}

search_parameters_for_both = {"search_by_gender": "Both", "search_by_age_to": 15, "search_by_age_from": 25}
search_parameters_for_girl = {"search_by_gender": "Girl", "search_by_age_to": 15, "search_by_age_from": 25}
incorrect_search_parameters = {"search_by_gender": "girl", "search_by_age_to": 14, "search_by_age_from": 81}
