from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.auth.dependencies import GetCurrentUser
from app.blacklist.schemas import UserIDRequestSchema
from app.blacklist.services import BlacklistServices
from app.blacklist.dependencies import GetBlacklistService
from app.users.schemas import UserMappingSchema


router = APIRouter(
    prefix="/blacklist",
    tags=["Blacklist"],
)


@router.post("/block")
async def add_user_to_blacklist(
        user_data: UserIDRequestSchema,
        user=GetCurrentUser,
        blacklist_services: BlacklistServices = GetBlacklistService,
):
    await blacklist_services.add_user_to_blacklist(user_id=user.id, blocked_user_id=user_data.user_id)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "User blocked"})


@router.post("/unblock")
async def remove_user_from_blacklist(
        user_data: UserIDRequestSchema,
        user=GetCurrentUser,
        blacklist_services: BlacklistServices = GetBlacklistService,
):
    await blacklist_services.remove_user_from_blacklist(user_id=user.id, blocked_user_id=user_data.user_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "User unblocked"})


@router.get("/list")
async def get_list_of_blacklisted_users(
        user=GetCurrentUser,
        blacklist_services: BlacklistServices = GetBlacklistService,
) -> List[UserMappingSchema]:
    return await blacklist_services.get_list_of_blacklisted_users(user_id=user.id)
