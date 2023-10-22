from sqlalchemy import update, select, func

from app.database import async_session_maker
from app.utils.repository import BaseRepository
from app.posts.models import Posts
from app.likes.models import Like


class PostsRepository(BaseRepository):
    model = Posts

    async def partial_update(self, post_id: int, author_id: int, **data):
        async with async_session_maker() as session:
            query = update(self.model).values(**data).filter_by(id=post_id, author_id=author_id).returning(self.model)
            result = await session.execute(query)
            await session.commit()
            return result.mappings().one()

    async def get_list_of_posts_with_likes(self, author_id=None, **filter_by):
        async with async_session_maker() as session:
            query = (
                select(
                    self.model.__table__.columns,
                    func.count(Like.__table__.columns.id).label('likes_count')
                )
                .outerjoin(Like, self.model.__table__.columns.id == Like.__table__.columns.post_id)
                .group_by(self.model.__table__.columns.id)
                .filter_by(**filter_by)
            ).order_by(self.model.__table__.columns.created_at.desc())

            if author_id:
                query = query.filter(self.model.__table__.columns.author_id == author_id)

            result = await session.execute(query)
            return result.mappings().all()
