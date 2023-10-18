from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from app.database import get_async_session
from app.users.repository import UserRepository, FriendShipRepository
from app.utils.dependencies import ActiveAsyncSession
from app.utils.exceptions import FriendShipAlreadyExists, FriendShipRequestAlreadyExists


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


class FriendShipServices:
    def __init__(self, friendship_repository: type[FriendShipRepository]):
        self.friendship_repository: FriendShipRepository = friendship_repository()

    async def send_friend_request(self, from_user_id, to_user_id):
        existing_friendship = await self.friendship_repository.find_one_or_none(
            from_user=to_user_id,
            to_user=from_user_id
        )

        if existing_friendship:
            if existing_friendship.is_accepted:
                raise FriendShipAlreadyExists
            else:
                return await self.friendship_repository.update(model_id=existing_friendship.id, is_accepted=True)

        try:
            return await self.friendship_repository.add(from_user=from_user_id, to_user=to_user_id)
        except IntegrityError:
            raise FriendShipRequestAlreadyExists

