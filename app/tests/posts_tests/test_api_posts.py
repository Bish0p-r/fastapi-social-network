import pytest

from httpx import AsyncClient


async def test_get_list_of_posts(ac: AsyncClient):
    response = await ac.get("/posts/list")

    assert response.status_code == 200
    assert len(response.json()) == 3


@pytest.mark.parametrize(
    "author_id,count_posts,status_code",
    [
        (1, 0, 200),
        (2, 2, 200),
        (3, 1, 200),
        (4, 0, 200),
        ('str', None, 422),
    ]
)
async def test_get_list_of_user_posts(author_id, count_posts, status_code, ac: AsyncClient):
    response = await ac.get(f"/posts/user-posts/{author_id}")

    assert response.status_code == status_code

    if count_posts is not None:
        assert len(response.json()) == count_posts


async def test_not_authorized_create_post(ac: AsyncClient):
    response = await ac.post("/posts/create", json={"title": "test_title_1", "content": "test_content_1"})

    assert response.status_code == 401


@pytest.mark.parametrize(
    "data,count_posts,status_code",
    [
        ({"title": "test_title_1", "content": "test_content_1"}, 4, 200),
        ({"title": None, "content": "test_content_1"}, 5, 200),
        ({"content": "test_content_1"}, 5, 422),
        ({"title": None, "content": 123}, 5, 422),
        ({"title": None, "content": "test_content_1", "extra_field": "test"}, 5, 422),
    ]
)
async def test_authorized_create_post(data, status_code, count_posts, authenticated_admin_ac: AsyncClient):
    response = await authenticated_admin_ac.post("/posts/create", json=data)

    assert response.status_code == status_code

    if status_code == 200:
        assert response.json()['Posts'].get("title") == data["title"]
        assert response.json()['Posts'].get("content") == data["content"]

    response = await authenticated_admin_ac.get("/posts/list")

    assert response.status_code == 200
    assert len(response.json()) == count_posts


async def test_not_authorized_partial_update_post(ac: AsyncClient):
    response = await ac.patch("/posts/update/1", json={"title": "test_title_1", "content": "test_content_1"})

    assert response.status_code == 401


@pytest.mark.parametrize(
    "post_id,data,status_code",
    [
        (1, {"title": "test", "content": "test_test"}, 200),
        (2, {"title": "test", "content": "test_test"}, 200),
        (2, {"content": "test_test"}, 200),
        (2, {"title": "test"}, 200),
        (3, {"title": "test", "content": "test_test"}, 400),
        (4, {"title": "test", "content": "test_test"}, 400),
        (1, {"title": 123, "content": "test_test"}, 422),
        (1, {"title": "test", "content": 123}, 422),
        (1, {"title": "test", "content": "test_test", "extra_field": "str"}, 422),
    ]
)
async def test_authorized_partial_update_post(post_id, data, status_code, authenticated_user_ac: AsyncClient):
    response = await authenticated_user_ac.patch(f"/posts/update/{post_id}", json=data)

    assert response.status_code == status_code

    if data.get("title") and status_code == 200:
        assert response.json()['Posts'].get("title") == data["title"]
    if data.get("content") and status_code == 200:
        assert response.json()['Posts'].get("content") == data["content"]


async def test_not_authorized_delete_post(ac: AsyncClient):
    response = await ac.delete("/posts/delete/1")

    assert response.status_code == 401


@pytest.mark.parametrize(
    "post_id,post_count,status_code",
    [
        (4, 4, 200),
        (5, 3, 200),
        (5, 3, 400),
        (2, 3, 400),
        ('str', 3, 422),
    ]
)
async def test_authorized_delete_post(post_id, status_code, post_count, authenticated_admin_ac: AsyncClient):
    response = await authenticated_admin_ac.delete(f"/posts/delete/{post_id}")

    assert response.status_code == status_code

    response = await authenticated_admin_ac.get("/posts/list")

    assert response.status_code == 200
    assert len(response.json()) == post_count

