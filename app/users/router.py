from typing import Annotated, List
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.users.services import UserServices, FriendShipServices
from app.users.schemas import UserSchema, MappingFriendShipSchema, FriendShipRequestSchema
from app.users.dependencies import GetUsersService, GetFriendShipService
from app.auth.dependencies import get_current_user
from app.utils.exceptions import FriendShipCannotBeSentToYourself


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/me")
async def me(user=Depends(get_current_user), user_services: UserServices = GetUsersService) -> UserSchema:
    return await user_services.get_user_by_id(user.id)


@router.get("/users")
async def get_list_of_users(user_services: UserServices = GetUsersService) -> List[UserSchema]:
    return await user_services.list_users()


@router.post("/users/send-friend-request")
async def send_friend_request(
        user_data: FriendShipRequestSchema,
        user=Depends(get_current_user),
        friendship_services: FriendShipServices = GetFriendShipService
) -> MappingFriendShipSchema:
    if user.id == user_data.to_user:
        raise FriendShipCannotBeSentToYourself
    return await friendship_services.send_friend_request(from_user_id=user.id, to_user_id=user_data.to_user)


@router.post("/users/cancel-sent-friend-request")
async def cancel_sent_friend_request(
        user_data: FriendShipRequestSchema,
        user=Depends(get_current_user),
        friendship_services: FriendShipServices = GetFriendShipService
):
    await friendship_services.cancel_sent_friend_request(from_user_id=user.id, to_user_id=user_data.to_user)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"message": "Friendship request canceled"})


@router.post("/users/accept-friend-request")
async def accept_friend_request(
        user_data: FriendShipRequestSchema,
        user=Depends(get_current_user),
        friendship_services: FriendShipServices = GetFriendShipService
):
    return await friendship_services.accept_friend_request(from_user_id=user_data.to_user, to_user_id=user.id)


@router.post("/users/reject-friend-request")
async def reject_friend_request(
        user_data: FriendShipRequestSchema,
        user=Depends(get_current_user),
        friendship_services: FriendShipServices = GetFriendShipService
):
    await friendship_services.cancel_sent_friend_request(from_user_id=user_data.to_user, to_user_id=user.id)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"message": "Friendship request rejected"})


@router.get("/users/me/friendships")
async def get_my_friendships(
        user=Depends(get_current_user),
        friendship_services: FriendShipServices = GetFriendShipService
) -> List[UserSchema]:
    return await friendship_services.get_list_of_friendships(user.id)
