from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.friendships.schemas import FriendShipRequestSchema, MappingFriendShipSchema
from app.friendships.dependencies import GetFriendShipService
from app.friendships.services import FriendShipServices
from app.auth.dependencies import get_current_user
from app.users.schemas import UserSchema


router = APIRouter(
    prefix="/friendships",
    tags=["Friendships"],
)


@router.get("")
async def test():
    pass


@router.post("/send-friend-request")
async def send_friend_request(
        user_data: FriendShipRequestSchema,
        user=Depends(get_current_user),
        friendship_services: FriendShipServices = GetFriendShipService
) -> MappingFriendShipSchema:
    return await friendship_services.send_friend_request(from_user_id=user.id, to_user_id=user_data.to_user)


@router.post("/cancel-sent-friend-request")
async def cancel_sent_friend_request(
        user_data: FriendShipRequestSchema,
        user=Depends(get_current_user),
        friendship_services: FriendShipServices = GetFriendShipService
):
    await friendship_services.cancel_sent_friend_request(from_user_id=user.id, to_user_id=user_data.to_user)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"message": "Friendship request canceled"})


@router.post("/accept-friend-request")
async def accept_friend_request(
        user_data: FriendShipRequestSchema,
        user=Depends(get_current_user),
        friendship_services: FriendShipServices = GetFriendShipService
):
    return await friendship_services.accept_friend_request(from_user_id=user_data.to_user, to_user_id=user.id)


@router.post("/reject-friend-request")
async def reject_friend_request(
        user_data: FriendShipRequestSchema,
        user=Depends(get_current_user),
        friendship_services: FriendShipServices = GetFriendShipService
):
    await friendship_services.cancel_sent_friend_request(from_user_id=user_data.to_user, to_user_id=user.id)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"message": "Friendship request rejected"})


@router.get("/me/friendships")
async def get_my_friendships(
        user=Depends(get_current_user),
        friendship_services: FriendShipServices = GetFriendShipService
) -> List[UserSchema]:
    return await friendship_services.get_list_of_friendships(user.id)