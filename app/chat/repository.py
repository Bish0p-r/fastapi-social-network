from sqlalchemy import or_, select, and_

from app.chat.models import Message
from app.database import async_session_maker
from app.utils.repository import BaseRepository


class MessagesRepository(BaseRepository):
    model = Message

    async def list_of_sent_messages(self, from_user: int, to_user: int):
        async with async_session_maker() as session:
            query = select(self.model.__table__.columns).filter(
                or_(
                    and_(self.model.from_user == from_user, self.model.to_user == to_user),
                    and_(self.model.from_user == to_user, self.model.to_user == from_user)
                ),
            )
            result = await session.execute(query)
            return result.mappings().all()
