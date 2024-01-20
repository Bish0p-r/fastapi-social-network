import pytest

from httpx import AsyncClient


async def test_not_authorized_get_list_of_blacklisted_users(ac: AsyncClient):
    response = await ac.get("/blacklist/")

    assert response.status_code == 401


async def test_authorized_get_list_of_blacklisted_users(authenticated_admin_ac: AsyncClient):
    response = await authenticated_admin_ac.get("/blacklist/")

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_not_authorized_add_user_to_blacklist(ac: AsyncClient):
    response = await ac.post("/blacklist/", json={"user_id": 3})

    assert response.status_code == 401


@pytest.mark.parametrize(
    "user_id,count_blocked_users,status_code",
    [
        (3, 2, 201),
        (3, 2, 400),
        ("str", 2, 422),
    ],
)
async def test_authorized_add_user_to_blacklist(
    user_id, count_blocked_users, status_code, authenticated_admin_ac: AsyncClient
):
    response = await authenticated_admin_ac.post("/blacklist/", json={"user_id": user_id})

    assert response.status_code == status_code

    if status_code == 200:
        response = await authenticated_admin_ac.get("/blacklist/")

        assert response.status_code == 200
        assert len(response.json()) == count_blocked_users


async def test_not_authorized_remove_user_from_blacklist(ac: AsyncClient):
    response = await ac.delete("/blacklist/3")

    assert response.status_code == 401


@pytest.mark.parametrize(
    "user_id,count_blocked_users,status_code", [(3, 1, 200), (3, 1, 400), ("str", 1, 422), (2, 0, 200)]
)
async def test_authorized_remove_user_from_blacklist(
    user_id, count_blocked_users, status_code, authenticated_admin_ac: AsyncClient
):
    response = await authenticated_admin_ac.delete(f"/blacklist/{user_id}")

    assert response.status_code == status_code

    response = await authenticated_admin_ac.get("/blacklist/")

    assert response.status_code == 200
    assert len(response.json()) == count_blocked_users
