from fastapi import Depends

from app.comments.repository import CommentsRepository
from app.comments.services import CommentsServices


async def comments_service():
    return CommentsServices(CommentsRepository)


GetCommentsService = Depends(comments_service)
