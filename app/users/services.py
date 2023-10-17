from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from app.database import get_async_session
from app.users.repository import UserRepository, UserProfileRepository
from app.utils.dependencies import ActiveAsyncSession


class UserServices:
    def __init__(self, user_repository: type[UserRepository]):
        self.user_repository: UserRepository = user_repository()

    async def list_users(self):
        return await self.user_repository.find_all()

    async def get_user_by_id(self, user_id):
        return await self.user_repository.find_one_or_none(id=user_id)

    async def get_user_by_email(self, user_email):
        return await self.user_repository.find_one_or_none(email=user_email)

    async def create_user(self, **user_data):
        return await self.user_repository.add(**user_data)

    async def activate_user(self, user_email):
        return await self.user_repository.update_by_email(user_email, is_active=True)


class UserProfileService:
    def __init__(self, profile_repository: type[UserProfileRepository]):
        self.profile_repository: UserProfileRepository = profile_repository()

    async def list_user_profiles(self):
        return await self.profile_repository.find_all()

    async def get_user_profile(self, user_id):
        return await self.profile_repository.find_one_or_none(user_id=user_id)

    async def create_user_profile(self, user_id, **profile_data):
        try:
            await self.profile_repository.add(user_id=user_id, **profile_data)
        except IntegrityError as e:
            print(e)
        # return await self.profile_repository.add(user_id=user_id, **profile_data)

