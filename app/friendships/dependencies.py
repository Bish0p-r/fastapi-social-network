from fastapi import Depends

from app.friendships.services import FriendShipServices
from app.friendships.repository import FriendShipRepository


async def friendship_service():
    return FriendShipServices(FriendShipRepository)


GetFriendShipService = Depends(friendship_service)
