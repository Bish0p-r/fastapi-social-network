from fastapi import Depends

from app.likes.repository import LikesRepository
from app.likes.services import LikesServices


async def likes_service():
    return LikesServices(LikesRepository)


GetLikesService = Depends(likes_service)
