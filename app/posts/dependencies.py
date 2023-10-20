from fastapi import Depends

from app.posts.services import PostsServices
from app.posts.repository import PostsRepository


async def posts_service():
    return PostsServices(PostsRepository)


GetPostsService = Depends(posts_service)
