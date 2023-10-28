import pytest
import json

from httpx import AsyncClient


async def test_get_my_profile(authenticated_admin_ac: AsyncClient):
    response = await authenticated_admin_ac.get("/users/me")

    assert response.status_code == 200
    assert response.json().get("email") == "test_admin@test.com"
    assert response.json().get("first_name") == "test_admin_first_name"
    assert response.json().get("last_name") == "test_admin_last_name"
    assert response.json().get("privacy_settings") == "public"


async def test_get_list_of_users(authenticated_admin_ac: AsyncClient):
    response = await authenticated_admin_ac.get("/users")

    assert response.status_code == 200
    assert len(response.json()) == 3


@pytest.mark.parametrize(
    "user_id,status_code",
    [
        (1, 200),
        (2, 200),
        (3, 200),
        (4, 400),
        (5, 400),
        ('str', 422),
        (None, 422),
    ]
)
async def test_get_user_by_id(user_id, status_code, authenticated_admin_ac: AsyncClient):
    response = await authenticated_admin_ac.get(f"/users/{user_id}")

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "data,status_code",
    [
        ({
            "first_name": "string",
            "last_name": "string",
            "privacy_settings": "public",
            "date_of_birth": "2023-10-27",
            "bio": "string"
         },
         200),
        ({
            "privacy_settings": "private",
            "date_of_birth": "2012-10-27",
            "bio": None
         },
         200),
        ({
             "privacy_settings": "wrong_enum"
         },
         422),
        ({
             "first_name": None,
             "last_name": None,
             "privacy_settings": None,
             "date_of_birth": None,
             "bio": None
         },
         422),
        ({
             "extra_field": "123"
         },
         422),
    ]
)
async def test_partial_update_user(data, status_code, authenticated_admin_ac: AsyncClient):
    response = await authenticated_admin_ac.patch("/users/update", json=data)

    assert response.status_code == status_code

    if status_code == 200:
        for k, v in data.items():
            assert response.json().get(k) == v

