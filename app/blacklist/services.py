from asyncpg import UniqueViolationError, ForeignKeyViolationError
from sqlalchemy.exc import IntegrityError

from app.blacklist.repository import BlacklistRepository
from app.utils.exceptions import IncorrectUserIdException, UserAlreadyInBlackListException


class BlacklistServices:
    def __init__(self, blacklist_repository: type[BlacklistRepository]):
        self.blacklist_repository: BlacklistRepository = blacklist_repository()

    async def add_user_to_blacklist(self, user_id: int, blocked_user_id: int):
        try:
            await self.blacklist_repository.add(initiator_user=user_id, blocked_user=blocked_user_id)
        except IntegrityError as e:
            if e.orig.__cause__.__class__ == UniqueViolationError:
                raise UserAlreadyInBlackListException
            elif e.orig.__cause__.__class__ == ForeignKeyViolationError:
                raise IncorrectUserIdException
            raise UserAlreadyInBlackListException

    async def remove_user_from_blacklist(self, user_id: int, blocked_user_id: int):
        await self.blacklist_repository.delete(initiator_user=user_id, blocked_user=blocked_user_id)

    async def get_list_of_blacklisted_users(self, user_id: int):
        return await self.blacklist_repository.list_blacklisted_users(user_id=user_id)
