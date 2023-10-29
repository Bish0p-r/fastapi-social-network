from sqlalchemy import select, insert, delete, update

from app.database import async_session_maker


class BaseRepository:
    model = None

    async def find_by_id(self, model_id: int):
        async with async_session_maker() as session:
            query = select(self.model.__table__.columns).filter_by(id=model_id)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    async def find_one_or_none(self, **filter_by):
        async with async_session_maker() as session:
            query = select(self.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    async def find_all(self, **filter_by):
        async with async_session_maker() as session:
            query = select(self.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()

    async def add(self, **data):
        async with async_session_maker() as session:
            query = insert(self.model).values(**data).returning(self.model)
            result = await session.execute(query)
            await session.commit()
            return result.mappings().one_or_none()

    async def delete(self, **filter_by):
        async with async_session_maker() as session:
            user_booked_rooms = delete(self.model).filter_by(**filter_by).returning(self.model)
            result = await session.execute(user_booked_rooms)
            await session.commit()
            return result.mappings().one_or_none()

    async def update(self, model_id: int, **data):
        async with async_session_maker() as session:
            query = update(self.model).values(**data).filter_by(id=model_id).returning(self.model.__table__.columns)
            result = await session.execute(query)
            await session.commit()
            return result.mappings().one_or_none()
