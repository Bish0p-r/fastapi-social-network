import pytest

from httpx import AsyncClient


async def test_not_authorized_get_my_friendships(ac: AsyncClient):
    response = await ac.get("/friendships/my-friends")

    assert response.status_code == 401


async def test_authorized_get_my_friendships(authenticated_admin_ac: AsyncClient):
    response = await authenticated_admin_ac.get("/friendships/my-friends")

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_not_authorized_send_friend_request(ac: AsyncClient):
    response = await ac.post("/friendships/send-friend-request", json={"user_id": 3})

    assert response.status_code == 401


@pytest.mark.parametrize(
    "user_id,status_code",
    [
        (2, 200),
        (2, 400),
        (1, 400),
        (3, 400),
        (None, 422),
        ("str", 422),
    ],
)
async def test_authorized_send_friend_request(user_id, status_code, authenticated_admin_ac: AsyncClient):
    response = await authenticated_admin_ac.post("/friendships/send-friend-request", json={"user_id": user_id})

    assert response.status_code == status_code


async def test_not_authorized_accept_friend_request(ac: AsyncClient):
    response = await ac.post("/friendships/accept-friend-request", json={"user_id": 3})

    assert response.status_code == 401


@pytest.mark.parametrize(
    "user_id,count_friends,status_code",
    [
        (7, 1, 400),
        (4, 2, 200),
        (None, 2, 422),
        ("str", 2, 422),
    ],
)
async def test_authorized_accept_friend_request(
    user_id, status_code, count_friends, authenticated_admin_ac: AsyncClient
):
    response = await authenticated_admin_ac.post("/friendships/accept-friend-request", json={"user_id": user_id})

    assert response.status_code == status_code

    response = await authenticated_admin_ac.get("/friendships/my-friends")

    assert response.status_code == 200
    assert len(response.json()) == count_friends


async def test_not_authorized_reject_friend_request(ac: AsyncClient):
    response = await ac.delete("/friendships/reject-friend-request/3")

    assert response.status_code == 401


@pytest.mark.parametrize(
    "user_id,status_code",
    [
        (5, 200),
        (5, 400),
        (1, 400),
        (None, 422),
        ("str", 422),
    ],
)
async def test_authorized_reject_friend_request(user_id, status_code, authenticated_admin_ac: AsyncClient):
    response = await authenticated_admin_ac.delete(f"/friendships/reject-friend-request/{user_id}")

    assert response.status_code == status_code


async def test_not_authorized_cancel_sent_friend_request(ac: AsyncClient):
    response = await ac.delete("/friendships/cancel-sent-friend-request/3")

    assert response.status_code == 401


@pytest.mark.parametrize(
    "user_id,status_code",
    [
        (2, 200),
        (2, 400),
        (1, 400),
        (None, 422),
        ("str", 422),
    ],
)
async def test_authorized_cancel_sent_friend_request(user_id, status_code, authenticated_admin_ac: AsyncClient):
    response = await authenticated_admin_ac.delete(f"/friendships/cancel-sent-friend-request/{user_id}")

    assert response.status_code == status_code


async def test_not_authorized_remove_friend(ac: AsyncClient):
    response = await ac.delete("/friendships/remove-friend/3")

    assert response.status_code == 401


@pytest.mark.parametrize(
    "user_id,count_friends,status_code",
    [
        (3, 1, 200),
        (3, 1, 400),
        (7, 1, 400),
        (4, 0, 200),
        (None, 0, 422),
        ("str", 0, 422),
    ],
)
async def test_authorized_remove_friend(user_id, status_code, count_friends, authenticated_admin_ac: AsyncClient):
    response = await authenticated_admin_ac.delete(f"/friendships/remove-friend/{user_id}")

    assert response.status_code == status_code

    response = await authenticated_admin_ac.get("/friendships/my-friends")

    assert response.status_code == 200
    assert len(response.json()) == count_friends
