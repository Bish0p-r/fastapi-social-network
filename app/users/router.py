from typing import List

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.users.services import UserServices
from app.users.schemas import UserSchema, UserUpdateSchema, UserFullInfoSchema
from app.users.dependencies import GetUsersService
from app.auth.dependencies import GetCurrentUser


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/me")
async def get_my_profile(user=GetCurrentUser, user_services: UserServices = GetUsersService) -> UserFullInfoSchema:
    return await user_services.get_my_full_info(user.id)


@router.get("")
@cache(expire=30)
async def get_list_of_users(user_services: UserServices = GetUsersService) -> List[UserSchema]:
    return await user_services.list_users()


@router.get("/{user_id}")
@cache(expire=30)
async def get_user_by_id(user_id: int, user_services: UserServices = GetUsersService) -> UserSchema | None:
    return await user_services.get_user_by_id(user_id)


@router.patch("/me")
async def partial_update_user(
    user_data: UserUpdateSchema, user=GetCurrentUser, user_services: UserServices = GetUsersService
) -> UserSchema:
    data = user_data.model_dump(exclude_unset=True)
    return await user_services.partial_update_user(user.id, **data)
