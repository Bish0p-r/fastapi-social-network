from typing import Annotated, List
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.users.services import UserServices
from app.users.schemas import UserSchema, UserUpdateSchema, UserMappingSchema, UserDetailsSchema
from app.users.dependencies import GetUsersService
from app.auth.dependencies import get_current_user, GetCurrentUser


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/me")
async def get_my_profile(
        user=GetCurrentUser
) -> UserDetailsSchema:
    return user


@router.get("")
async def get_list_of_users(
        user_services: UserServices = GetUsersService
) -> List[UserSchema]:
    return await user_services.list_users()


@router.get("/{user_id}")
async def get_user_by_id(
        user_id: int,
        user_services: UserServices = GetUsersService
) -> UserSchema | None:
    return await user_services.get_user_by_id(user_id)


@router.patch("/update")
async def partial_update_user(
        user_data: UserUpdateSchema,
        user=GetCurrentUser,
        user_services: UserServices = GetUsersService
) -> UserMappingSchema:
    data = user_data.model_dump(exclude_unset=True)
    print(data)
    return await user_services.partial_update_user(user.id, **data)
