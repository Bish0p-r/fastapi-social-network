import pytest

from httpx import AsyncClient


async def test_not_authorized_get_list_of_my_comments(ac: AsyncClient):
    response = await ac.get("/comments/my-comments")

    assert response.status_code == 401


async def test_authorized_get_list_of_my_comments(authenticated_user_ac):
    response = await authenticated_user_ac.get("/comments/my-comments")

    assert response.status_code == 200
    assert len(response.json()) == 3


@pytest.mark.parametrize(
    "post_id,count_comments,status_code",
    [
        (1, 3, 200),
        (2, 1, 200),
        (3, 0, 200),
        (123, 0, 200),
        ("str", 0, 422),
    ],
)
async def test_get_list_of_comments_by_post_id(post_id, count_comments, status_code, ac: AsyncClient):
    response = await ac.get(f"/comments/post-comments/{post_id}")

    assert response.status_code == status_code
    if status_code == 200:
        assert len(response.json()) == count_comments


async def test_not_authorized_create_comment(ac: AsyncClient):
    response = await ac.post("/comments/", json={"post_id": 1, "text": "string"})

    assert response.status_code == 401


@pytest.mark.parametrize(
    "post_id,text,count_comments,status_code",
    [
        (1, "string", 4, 200),
        (1, "string", 5, 200),
        (2, "string", 2, 200),
        (3, "string", 1, 200),
        (123, "string", 5, 400),
        (1, None, 5, 422),
    ],
)
async def test_authorized_create_comment(
    post_id, text, count_comments, status_code, authenticated_admin_ac: AsyncClient
):
    response = await authenticated_admin_ac.post("/comments/", json={"post_id": post_id, "text": text})

    assert response.status_code == status_code

    if status_code == 200:
        assert response.json()["Comment"].get("text") == text

        response = await authenticated_admin_ac.get(f"/comments/post-comments/{post_id}")

        assert response.status_code == 200
        assert len(response.json()) == count_comments


async def test_not_authorized_delete_comment(ac: AsyncClient):
    response = await ac.delete("/comments/1")

    assert response.status_code == 401


@pytest.mark.parametrize(
    "comment_id,count_comments,status_code",
    [
        (3, 4, 200),
        (8, 3, 200),
        (7, 2, 200),
        (123, 2, 400),
        ("str", 2, 422),
    ],
)
async def test_authorized_delete_comment(comment_id, status_code, count_comments, authenticated_admin_ac: AsyncClient):
    response = await authenticated_admin_ac.delete(f"/comments/{comment_id}")

    assert response.status_code == status_code

    response = await authenticated_admin_ac.get("/comments/my-comments")

    assert response.status_code == 200
    assert len(response.json()) == count_comments
