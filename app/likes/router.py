from typing import List

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi_cache.decorator import cache

from app.auth.dependencies import GetCurrentUser
from app.likes.services import LikesServices
from app.likes.dependencies import GetLikesService
from app.posts.dependencies import GetPostsService
from app.posts.services import PostsServices
from app.users.schemas import UserMappingSchema
from app.posts.schemas import MappingPostSchema
from app.users.models import Users


router = APIRouter(
    prefix="/likes",
    tags=["Likes"],
)


@router.get("/my-liked-posts")
@cache(expire=30)
async def get_my_liked_posts(
    user: Users = GetCurrentUser, likes_services: LikesServices = GetLikesService
) -> List[MappingPostSchema]:
    return await likes_services.get_list_user_liked_posts(user_id=user.id)


@router.get("/post-likes/{post_id}")
async def get_list_of_users_who_liked_the_post(
    post_id: int, likes_services: LikesServices = GetLikesService
) -> List[UserMappingSchema]:
    return await likes_services.get_list_of_users(post_id=post_id)


@router.post("/like/{post_id}")
async def like_the_post(
    post_id: int,
    user: Users = GetCurrentUser,
    likes_services: LikesServices = GetLikesService,
    post_services: PostsServices = GetPostsService,
):
    await post_services.check_permission(post_id=post_id, black_list=user.im_blacklisted)
    await likes_services.create_like(user_id=user.id, post_id=post_id)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": f"Post #{post_id} liked"})


@router.delete("/unlike/{post_id}")
async def unlike_the_post(post_id: int, user: Users = GetCurrentUser, likes_services: LikesServices = GetLikesService):
    await likes_services.delete_like(user_id=user.id, post_id=post_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": f"Like for post #{post_id} was removed"})
