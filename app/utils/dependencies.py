from fastapi import Depends
from redis import asyncio as aioredis

from app.database import get_async_session
from app.config import settings


ActiveAsyncSession = Depends(get_async_session)


async def get_redis() -> aioredis.Redis:
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", encoding="utf8", decode_responses=True
    )
    try:
        yield redis
    finally:
        await redis.close()


GetRedis = Depends(get_redis)
