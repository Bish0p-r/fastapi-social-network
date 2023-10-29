from sqlalchemy import select

from app.database import async_session_maker
from app.utils.repository import BaseRepository
from app.likes.models import Like
from app.posts.models import Posts
from app.users.models import Users


class LikesRepository(BaseRepository):
    model = Like

    async def list_liked_posts(self, **filter_by):
        async with async_session_maker() as session:
            query = select(Posts).join(self.model, self.model.post_id == Posts.id).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()

    async def list_users_who_liked_post(self, **filter_by):
        async with async_session_maker() as session:
            query = select(Users).join(self.model, self.model.user_id == Users.id).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()
