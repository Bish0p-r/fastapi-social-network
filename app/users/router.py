from typing import Annotated, List
from fastapi import APIRouter, Depends

from app.users.services import UserServices, FriendShipServices
from app.users.schemas import UserSchema, MappingFriendShipSchema
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
        to_user_id: int,
        user=Depends(get_current_user),
        friendship_services: FriendShipServices = GetFriendShipService
) -> MappingFriendShipSchema:
    if user.id == to_user_id:
        raise FriendShipCannotBeSentToYourself
    return await friendship_services.send_friend_request(from_user_id=user.id, to_user_id=to_user_id)


@router.post("/users/{user_id}/cancel-sent-friend-request")
async def cancel_sent_friend_request(user=Depends(get_current_user), user_services: UserServices = GetUsersService):
    pass


@router.post("/users/{user_id}/accept-friend-request")
async def accept_friend_request(user=Depends(get_current_user), user_services: UserServices = GetUsersService):
    pass


@router.post("/users/{user_id}/reject-friend-request")
async def reject_friend_request(user=Depends(get_current_user), user_services: UserServices = GetUsersService):
    pass
