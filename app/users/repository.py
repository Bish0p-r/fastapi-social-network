from sqlalchemy import update, select, or_, func, and_
from sqlalchemy.orm import joinedload

from app.blacklist.models import Blacklist
from app.utils.repository import BaseRepository
from app.users.models import Users
from app.database import async_session_maker


class UserRepository(BaseRepository):
    model = Users

    async def update_by_email(self, user_email: str, **data):
        async with async_session_maker() as session:
            query = update(self.model).values(**data).filter_by(email=user_email).returning(self.model)
            result = await session.execute(query)
            await session.commit()
            return result.mappings().one_or_none()

    async def find_one_or_none_with_blacklist(self, id: int):
        async with async_session_maker() as session:
            blacklist_subquery = (
                select(func.array_agg(Blacklist.initiator_user))
                .where(Blacklist.blocked_user == id)
                .scalar_subquery()
            )

            query = (
                select(Users.__table__.columns, blacklist_subquery.label("im_blacklisted"))
                .outerjoin(
                    Blacklist,
                    Users.id == Blacklist.blocked_user
                )
                .filter(Users.id == id)
                .group_by(Users.id)
            )
            result = await session.execute(query)
            result = result.mappings().one_or_none()
            return result

    async def get_my_full_info(self, model_id: int):
        async with async_session_maker() as session:
            query = select(
                self.model
            ).options(
                joinedload(self.model.posts),
                joinedload(self.model.liked_posts),
                joinedload(self.model.commented_posts),
                joinedload(self.model.outgoing_requests),
                joinedload(self.model.incoming_requests),
                joinedload(self.model.im_blacklisted),
                joinedload(self.model.my_blacklist),
            ).filter(self.model.id == model_id)

            return await session.scalar(query)
