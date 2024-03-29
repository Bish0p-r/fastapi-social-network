from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError

from app.friendships.repository import FriendShipRepository
from app.utils.exceptions import (
    FriendShipAlreadyExists,
    FriendShipRequestAlreadyExists,
    FriendShipCannotBeSentToYourself,
    IncorrectUserIdException,
    YouHaveBeenBlackListedException,
    FriendShipRequestDoesNotExists,
    FriendShipDoesNotExists,
)


class FriendShipServices:
    def __init__(self, friendship_repository: type[FriendShipRepository]):
        self.friendship_repository: FriendShipRepository = friendship_repository()

    async def send_friend_request(self, from_user_id, to_user_id):
        if from_user_id == to_user_id:
            raise FriendShipCannotBeSentToYourself

        existing_friendship = await self.friendship_repository.find_one_or_none(
            from_user=to_user_id, to_user=from_user_id
        )
        if existing_friendship:
            if existing_friendship.is_accepted:
                raise FriendShipAlreadyExists
            else:
                return await self.friendship_repository.update(model_id=existing_friendship.id, is_accepted=True)

        try:
            return await self.friendship_repository.add(from_user=from_user_id, to_user=to_user_id)
        except IntegrityError as e:
            if e.orig.__cause__.__class__ == UniqueViolationError:
                raise FriendShipRequestAlreadyExists
            elif e.orig.__cause__.__class__ == ForeignKeyViolationError:
                raise IncorrectUserIdException
            raise FriendShipRequestAlreadyExists

    async def cancel_sent_friend_request(self, from_user_id, to_user_id):
        result = await self.friendship_repository.delete(from_user=from_user_id, to_user=to_user_id, is_accepted=False)
        if result is None:
            raise FriendShipRequestDoesNotExists
        return result

    async def delete_accepted_friend_request(self, from_user_id, to_user_id):
        result = await self.friendship_repository.delete_accepted_friend_request(
            user1_id=from_user_id, user2_id=to_user_id
        )
        if result is None:
            raise FriendShipDoesNotExists
        return result

    async def accept_friend_request(self, from_user_id, to_user_id):
        result = await self.friendship_repository.update_by_users_id(
            from_user_id=from_user_id, to_user_id=to_user_id, is_accepted=True
        )
        if result is None:
            raise FriendShipRequestDoesNotExists
        return result

    async def get_list_of_friendships(self, user_id):
        return await self.friendship_repository.list_user_friendships(user_id=user_id)

    async def check_permission(self, user_id, blacklist: list = None):
        if blacklist and user_id in blacklist:
            raise YouHaveBeenBlackListedException
