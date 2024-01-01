import pytest

from httpx import AsyncClient


async def test_not_authorized_get_my_liked_posts(ac: AsyncClient):
    response = await ac.get("/likes/my-liked-posts")

    assert response.status_code == 401


async def test_authorized_get_my_liked_posts(authenticated_admin_ac: AsyncClient):
    response = await authenticated_admin_ac.get("/likes/my-liked-posts")

    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.parametrize(
    "post_id,count_likes,status_code",
    [
        (1, 2, 200),
        (2, 1, 200),
        (3, 0, 200),
        ("str", 0, 422),
    ],
)
async def test_get_list_of_users_who_liked_the_post(post_id, count_likes, status_code, ac: AsyncClient):
    response = await ac.get(f"/likes/post-likes/{post_id}")

    assert response.status_code == status_code

    if status_code == 200:
        assert len(response.json()) == count_likes


async def test_not_authorized_like_the_post(ac: AsyncClient):
    response = await ac.post("/likes/1")

    assert response.status_code == 401


@pytest.mark.parametrize(
    "post_id,count_likes,status_code",
    [
        (2, 2, 201),
        (3, 3, 201),
        (2, 3, 400),
        (3, 3, 400),
        ("str", 3, 422),
    ],
)
async def test_authorized_like_the_post(post_id, count_likes, status_code, authenticated_admin_ac: AsyncClient):
    response = await authenticated_admin_ac.post(f"/likes/{post_id}")

    assert response.status_code == status_code

    response = await authenticated_admin_ac.get("/likes/my-liked-posts")

    assert response.status_code == 200
    assert len(response.json()) == count_likes


async def test_not_authorized_unlike_the_post(ac: AsyncClient):
    response = await ac.delete("/likes/1")

    assert response.status_code == 401


@pytest.mark.parametrize(
    "post_id,count_likes,status_code",
    [
        (2, 2, 200),
        (3, 1, 200),
        (1, 0, 200),
        (3, 0, 400),
        ("str", 0, 422),
    ],
)
async def test_authorized_unlike_the_post(post_id, count_likes, status_code, authenticated_admin_ac: AsyncClient):
    response = await authenticated_admin_ac.delete(f"/likes/{post_id}")

    assert response.status_code == status_code

    response = await authenticated_admin_ac.get("/likes/my-liked-posts")

    assert response.status_code == 200
    assert len(response.json()) == count_likes
