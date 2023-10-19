from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from app.database import get_async_session
from app.users.repository import UserRepository
from app.utils.dependencies import ActiveAsyncSession
from app.utils.exceptions import FriendShipAlreadyExists, FriendShipRequestAlreadyExists, \
    FriendShipCannotBeSentToYourself


class UserServices:
    def __init__(self, user_repository: type[UserRepository]):
        self.user_repository: UserRepository = user_repository()

    async def list_users(self, is_active=True, **filter_by):
        return await self.user_repository.find_all(is_active=is_active, **filter_by)

    async def get_user_by_id(self, user_id):
        return await self.user_repository.find_one_or_none(id=user_id)

    async def get_user_by_email(self, user_email):
        return await self.user_repository.find_one_or_none(email=user_email)

    async def create_user(self, **user_data):
        return await self.user_repository.add(**user_data)

    async def activate_user(self, user_email):
        return await self.user_repository.update_by_email(user_email, is_active=True)

