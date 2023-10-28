from asyncpg import UniqueViolationError, ForeignKeyViolationError
from sqlalchemy.exc import IntegrityError

from app.likes.repository import LikesRepository
from app.utils.exceptions import YouHaveAlreadyLikedThisPostException, IncorrectPostIdException


class LikesServices:
    def __init__(self, likes_repository: type[LikesRepository]):
        self.likes_repository: LikesRepository = likes_repository()

    async def get_list_user_liked_posts(self, user_id):
        return await self.likes_repository.list_liked_posts(user_id=user_id)

    async def get_list_of_users(self, post_id):
        return await self.likes_repository.list_users_who_liked_post(post_id=post_id)

    async def create_like(self, user_id, post_id):
        try:
            return await self.likes_repository.add(user_id=user_id, post_id=post_id)
        except IntegrityError as e:
            if e.orig.__cause__.__class__ == UniqueViolationError:
                raise YouHaveAlreadyLikedThisPostException
            elif e.orig.__cause__.__class__ == ForeignKeyViolationError:
                raise IncorrectPostIdException
            raise IncorrectPostIdException

    async def delete_like(self, user_id, post_id):
        result = await self.likes_repository.delete(user_id=user_id, post_id=post_id)
        if result is None:
            raise IncorrectPostIdException
