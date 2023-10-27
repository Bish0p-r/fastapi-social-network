import pytest
import json
import asyncio

from sqlalchemy import insert
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.config import settings
from app.database import Base, async_session_maker, async_engine
from app.main import app as fastapi_app
from app.users.models import Users
from app.posts.models import Posts
from app.comments.models import Comment
from app.likes.models import Like
from app.friendships.models import Friendships
from app.blacklist.models import Blacklist


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_data/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    users = open_mock_json("users")
    posts = open_mock_json("posts")
    likes = open_mock_json("likes")
    comments = open_mock_json("comments")
    friendships = open_mock_json("friendships")
    blacklists = open_mock_json("blacklists")

    async with async_session_maker() as session:
        add_users = insert(Users).values(users)
        add_posts = insert(Posts).values(posts)
        add_likes = insert(Like).values(likes)
        add_comments = insert(Comment).values(comments)
        add_friendships = insert(Friendships).values(friendships)
        add_blacklists = insert(Blacklist).values(blacklists)

        await session.execute(add_users)
        await session.execute(add_posts)
        await session.execute(add_likes)
        await session.execute(add_comments)
        await session.execute(add_friendships)
        await session.execute(add_blacklists)

        await session.commit()


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="function")
async def authenticated_ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        await ac.post("/auth/login", json={
            "email": "test_admin@test.com",
            "password": "test_admin_password"
        })
        assert ac.cookies["sn_access_token"]
        yield ac


@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session
