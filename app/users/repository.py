from sqlalchemy import update

from app.utils.repository import BaseRepository
from app.users.models import Users, Friendships
from app.database import async_session_maker


class UserRepository(BaseRepository):
    model = Users

    async def update_by_email(self, email: str, **data):
        async with async_session_maker() as session:
            query = update(self.model).values(**data).filter_by(email=email).returning(self.model)
            result = await session.execute(query)
            await session.commit()
            return result.mappings().one_or_none()


class FriendShipRepository(BaseRepository):
    model = Friendships
