from fastapi import Depends

from app.users.services import UserServices, FriendShipServices
from app.users.repository import UserRepository, FriendShipRepository


async def users_service():
    return UserServices(UserRepository)


GetUsersService = Depends(users_service)


async def friendship_service():
    return FriendShipServices(FriendShipRepository)


GetFriendShipService = Depends(friendship_service)
