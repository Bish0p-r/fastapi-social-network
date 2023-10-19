from sqlalchemy import select

from app.blacklist.models import Blacklist
from app.database import async_session_maker
from app.users.models import Users
from app.utils.repository import BaseRepository


class BlacklistRepository(BaseRepository):
    model = Blacklist

    async def list_blacklisted_users(self, user_id: int):
        async with async_session_maker() as session:
            query = select(Users).join(
                self.model,
                self.model.blocked_user == Users.id
            ).filter(
                self.model.initiator_user == user_id
            )
            result = await session.execute(query)
            return result.mappings().all()
