from typing import Annotated
from fastapi import APIRouter, Depends

from app.users.services import UserServices
from app.users.schemas import UserProfileSchema
from app.users.dependencies import GetUsersService
from app.auth.dependencies import get_current_user


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/me")
async def me(user=Depends(get_current_user), user_services: UserServices = GetUsersService) -> UserProfileSchema:
    # user = await user_services.get_user_by_id(user.id)
    return await user_services.get_user_by_id(user.id)


@router.get("/test")
async def test(user_services: UserServices = GetUsersService):
    r = await user_services.list_users()
    return r
