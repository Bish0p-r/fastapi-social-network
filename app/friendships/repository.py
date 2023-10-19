from sqlalchemy import update, select, or_

from app.utils.repository import BaseRepository
from app.friendships.models import Friendships
from app.users.models import Users
from app.database import async_session_maker


class FriendShipRepository(BaseRepository):
    model = Friendships

    async def update_by_users_id(self, from_user_id: int, to_user_id: int, **data):
        async with async_session_maker() as session:
            query = update(self.model).values(**data).filter_by(
                from_user=from_user_id, to_user=to_user_id
            ).returning(self.model)
            result = await session.execute(query)
            await session.commit()
            return result.mappings().one_or_none()

    async def list_user_friendships(self, user_id: int):
        async with async_session_maker() as session:
            user_q = select(Users).filter_by(id=user_id)
            query = select(Users).join(
                self.model,
                or_(self.model.to_user == Users.id, self.model.from_user == Users.id)
            ).filter(
                or_(self.model.from_user == user_id, self.model.to_user == user_id),
                self.model.is_accepted == True
            ).except_(user_q)
            result = await session.execute(query)
            return result.mappings().all()
