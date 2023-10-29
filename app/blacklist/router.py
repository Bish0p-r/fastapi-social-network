from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi_cache.decorator import cache

from app.auth.dependencies import GetCurrentUser
from app.blacklist.schemas import UserIDRequestSchema
from app.blacklist.services import BlacklistServices
from app.blacklist.dependencies import GetBlacklistService
from app.users.schemas import UserMappingSchema


router = APIRouter(
    prefix="/blacklist",
    tags=["Blacklist"],
)


@router.get("/list")
@cache(expire=30)
async def get_list_of_blacklisted_users(
        user=GetCurrentUser,
        blacklist_services: BlacklistServices = GetBlacklistService,
) -> List[UserMappingSchema]:
    return await blacklist_services.get_list_of_blacklisted_users(user_id=user.id)


@router.post("/block")
async def add_user_to_blacklist(
        user_data: UserIDRequestSchema,
        user=GetCurrentUser,
        blacklist_services: BlacklistServices = GetBlacklistService,
):
    await blacklist_services.add_user_to_blacklist(user_id=user.id, blocked_user_id=user_data.user_id)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "User blocked"})


@router.delete("/unblock/{user_id}")
async def remove_user_from_blacklist(
        user_id: int,
        user=GetCurrentUser,
        blacklist_services: BlacklistServices = GetBlacklistService,
):
    await blacklist_services.remove_user_from_blacklist(user_id=user.id, blocked_user_id=user_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": f"User #{user_id} was unblocked"},
    )
