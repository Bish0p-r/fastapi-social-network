from typing import List

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi_cache.decorator import cache

from app.auth.dependencies import GetCurrentUser
from app.posts.services import PostsServices
from app.posts.dependencies import GetPostsService
from app.posts.schemas import (
    PostDataRequestSchema,
    MappingPostSchema,
    PostDataResponseSchema,
    PostUpdateRequestSchema,
)


router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


@router.get("/")
@cache(expire=30)
async def get_list_of_posts(post_services: PostsServices = GetPostsService) -> List[PostDataResponseSchema]:
    return await post_services.get_list_of_posts()


@router.get("/user-posts/{author_id}")
@cache(expire=10)
async def get_list_of_user_posts(
    author_id: int, post_services: PostsServices = GetPostsService
) -> List[PostDataResponseSchema]:
    return await post_services.get_list_of_posts(author_id=author_id)


@router.post("/")
async def create_post(
    post_data: PostDataRequestSchema, user=GetCurrentUser, post_services: PostsServices = GetPostsService
) -> MappingPostSchema:
    return await post_services.create_post(author_id=user.id, title=post_data.title, content=post_data.content)


@router.patch("/{post_id}")
async def partial_update_post(
    post_id: int,
    post_data: PostUpdateRequestSchema,
    user=GetCurrentUser,
    post_services: PostsServices = GetPostsService,
) -> MappingPostSchema:
    data = post_data.model_dump(exclude_unset=True)
    return await post_services.partial_update_post(author_id=user.id, post_id=post_id, **data)


@router.delete("/{post_id}")
async def delete_post(post_id: int, user=GetCurrentUser, post_services: PostsServices = GetPostsService):
    await post_services.delete_post(author_id=user.id, post_id=post_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": f"Post #{post_id} was deleted"})
