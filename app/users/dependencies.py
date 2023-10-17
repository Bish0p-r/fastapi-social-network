from fastapi import Depends

from app.users.services import UserServices, UserProfileService
from app.users.repository import UserRepository, UserProfileRepository


async def users_service():
    return UserServices(UserRepository)


GetUsersService = Depends(users_service)


async def profile_service():
    return UserProfileService(UserProfileRepository)


GetProfileService = Depends(profile_service)
