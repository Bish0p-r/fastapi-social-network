from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi_cache.decorator import cache

from app.friendships.schemas import FriendShipRequestSchema, MappingFriendShipSchema
from app.friendships.dependencies import GetFriendShipService
from app.friendships.services import FriendShipServices
from app.auth.dependencies import GetCurrentUser
from app.users.schemas import UserSchema
from app.users.models import Users


router = APIRouter(
    prefix="/friendships",
    tags=["Friendships"],
)


@router.get("/me/friendships")
@cache(expire=30)
async def get_my_friendships(
        user: Users = GetCurrentUser,
        friendship_services: FriendShipServices = GetFriendShipService
) -> List[UserSchema]:
    return await friendship_services.get_list_of_friendships(user.id)


@router.post("/send-friend-request")
async def send_friend_request(
        user_data: FriendShipRequestSchema,
        user: Users = GetCurrentUser,
        friendship_services: FriendShipServices = GetFriendShipService
) -> MappingFriendShipSchema:
    return await friendship_services.send_friend_request(from_user_id=user.id, to_user_id=user_data.user_id)


@router.post("/accept-friend-request")
async def accept_friend_request(
        user_data: FriendShipRequestSchema,
        user: Users = GetCurrentUser,
        friendship_services: FriendShipServices = GetFriendShipService
):
    await friendship_services.check_permission(user.id, user.im_blacklisted)
    return await friendship_services.accept_friend_request(from_user_id=user_data.user_id, to_user_id=user.id)


@router.delete("/reject-friend-request")
async def reject_friend_request(
        user_data: FriendShipRequestSchema,
        user: Users = GetCurrentUser,
        friendship_services: FriendShipServices = GetFriendShipService
):
    await friendship_services.cancel_sent_friend_request(from_user_id=user_data.user_id, to_user_id=user.id)
    return status.HTTP_204_NO_CONTENT


@router.delete("/cancel-sent-friend-request")
async def cancel_sent_friend_request(
        user_data: FriendShipRequestSchema,
        user: Users = GetCurrentUser,
        friendship_services: FriendShipServices = GetFriendShipService
):
    await friendship_services.cancel_sent_friend_request(from_user_id=user.id, to_user_id=user_data.user_id)
    return status.HTTP_204_NO_CONTENT


@router.delete("/remove-friend")
async def remove_friend(
        user_data: FriendShipRequestSchema,
        user: Users = GetCurrentUser,
        friendship_services: FriendShipServices = GetFriendShipService
):
    await friendship_services.delete_accepted_friend_request(from_user_id=user.id, to_user_id=user_data.user_id)
    return status.HTTP_204_NO_CONTENT
