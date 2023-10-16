from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.config import settings


DATABASE_URL = settings.db_url

async_engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator:
    async with async_session_maker() as session:
        yield session


class Base(DeclarativeBase):
    pass
