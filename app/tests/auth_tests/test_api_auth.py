import pytest

from httpx import AsyncClient


@pytest.mark.parametrize(
    "email,password,confirm_password,first_name,last_name,users_count,status_code",
    [
         ("test-test@test.com", "testtest", "testtest", "test_first_name", "test_last_name", 5, 201),
         ("test-test2@test.com", "testtest", "testtest", "test_first_name", "test_last_name", 5, 201),
         ("test-test@test.com", "testtest", "testtest", "test_first_name", "test_last_name", 5, 409),
         ("test-test", "testtest", "testtest", "test_first_name", "test_last_name", 5, 422),
         ("test-test@test.com", "123", "123", "test_first_name", "test_last_name", 5, 422),
         ("test-test3@test.com", "testtest", "testtest", None, "test_last_name", 5, 422),
         ("test-test3@test.com", "testtest", "testtest", "test_first_name", None, 5, 422),
    ])
async def test_register_user(
        email,
        password,
        confirm_password,
        first_name,
        last_name,
        users_count,
        status_code,
        ac: AsyncClient
):
    response = await ac.post("/auth/register", json={
        "email": email,
        "password": password,
        "confirm_password": confirm_password,
        "first_name": first_name,
        "last_name": last_name
    })

    assert response.status_code == status_code

    response = await ac.get("/users")

    assert len(response.json()) == users_count


@pytest.mark.parametrize(
    "email,password,status_code,profile_status_code",
    [
        ("test_admin@test.com", "test_admin_wrong_password", 400, 401),
        ("test_wrong_admin@test.com", "test_admin_password", 400, 401),
        ("test_wrong_admin@test.com", "1", 422, 401),
        ("wrong_email", "test_admin_password", 422, 401),
        ("test_admin@test.com", "test_admin_password", 200, 200),
        ("test_user1@test.com", "test_password1", 200, 200),
    ])
async def test_login_user(
        email, password,
        status_code,
        profile_status_code,
        ac: AsyncClient
):
    response = await ac.post("/auth/login", json={
        "email": email,
        "password": password
    })

    assert response.status_code == status_code

    response = await ac.get("/users/me")

    assert response.status_code == profile_status_code


async def test_logout_user(authenticated_admin_ac: AsyncClient):
    assert authenticated_admin_ac.cookies["sn_access_token"]

    response = await authenticated_admin_ac.post("/auth/logout")

    assert response.status_code == 200
    assert response.cookies.get("sn_access_token") is None
