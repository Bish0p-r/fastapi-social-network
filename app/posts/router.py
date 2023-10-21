from typing import List

from fastapi import APIRouter

from app.auth.dependencies import GetCurrentUser
from app.posts.services import PostsServices
from app.posts.dependencies import GetPostsService
from app.posts.schemas import (
    PostDataRequestSchema,
    PostIDRequestSchema,
    MappingPostSchema,
    PostDataResponseSchema,
    PostAuthorIDRequestSchema,
    PostUpdateRequestSchema,
)


router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


@router.get("/list")
async def get_list_of_posts(
    post_services: PostsServices = GetPostsService
) -> List[PostDataResponseSchema]:
    return await post_services.get_list_of_posts()


@router.get("/user-posts")
async def get_list_of_user_posts(
    author_data: PostAuthorIDRequestSchema,
    post_services: PostsServices = GetPostsService
) -> List[PostDataResponseSchema]:
    return await post_services.get_list_of_posts(author=author_data.id)


@router.post("/create")
async def create_post(
    post_data: PostDataRequestSchema,
    user=GetCurrentUser,
    post_services: PostsServices = GetPostsService
) -> MappingPostSchema:
    return await post_services.create_post(author_id=user.id, title=post_data.title, content=post_data.content)


@router.patch("/update/{post_id}")
async def partial_update_post(
    post_id: int,
    post_data: PostUpdateRequestSchema,
    user=GetCurrentUser,
    post_services: PostsServices = GetPostsService
) -> MappingPostSchema:
    data = post_data.model_dump(exclude_unset=True)
    return await post_services.partial_update_post(author_id=user.id, post_id=post_id, **data)


@router.delete("/delete")
async def delete_post(
    post_data: PostIDRequestSchema,
    user=GetCurrentUser,
    post_services: PostsServices = GetPostsService
):
    await post_services.delete_post(author_id=user.id, post_id=post_data.id)

