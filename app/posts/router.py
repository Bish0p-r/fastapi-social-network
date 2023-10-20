from typing import List

from fastapi import APIRouter

from app.auth.dependencies import GetCurrentUser
from app.posts.services import PostsServices
from app.posts.dependencies import GetPostsService
from app.posts.schemas import PostDataRequestSchema, PostIDRequestSchema, MappingPostSchema, PostDataResponseSchema


router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


@router.get("/list")
async def get_list_of_posts(
    post_services: PostsServices = GetPostsService
) -> List[PostDataResponseSchema]:
    return await post_services.get_list_of_posts()


@router.post("/create")
async def create_post(
    post_data: PostDataRequestSchema,
    user=GetCurrentUser,
    post_services: PostsServices = GetPostsService
) -> MappingPostSchema:
    return await post_services.create_post(author_id=user.id, title=post_data.title, content=post_data.content)


@router.delete("/delete")
async def delete_post(
    post_data: PostIDRequestSchema,
    user=GetCurrentUser,
    post_services: PostsServices = GetPostsService
):
    await post_services.delete_post(author_id=user.id, post_id=post_data.id)

