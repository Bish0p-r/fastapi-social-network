from fastapi import Depends

from app.users.services import UserServices
from app.users.repository import UserRepository


async def users_service():
    return UserServices(UserRepository)


GetUsersService = Depends(users_service)
