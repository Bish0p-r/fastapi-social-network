from fastapi import Depends

from app.blacklist.repository import BlacklistRepository
from app.blacklist.services import BlacklistServices


async def blacklist_service():
    return BlacklistServices(BlacklistRepository)


GetBlacklistService = Depends(blacklist_service)
