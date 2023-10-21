from sqlalchemy import update

from app.database import async_session_maker
from app.utils.repository import BaseRepository
from app.posts.models import Posts


class PostsRepository(BaseRepository):
    model = Posts

    async def partial_update(self, post_id: int, author_id: int, **data):
        async with async_session_maker() as session:
            query = update(self.model).values(**data).filter_by(id=post_id, author_id=author_id).returning(self.model)
            result = await session.execute(query)
            await session.commit()
            return result.mappings().one()
