from typing import List

from fastapi import APIRouter

from app.auth.dependencies import GetCurrentUser
from app.comments.dependencies import GetCommentsService
from app.comments.services import CommentsServices
from app.posts.dependencies import GetPostsService
from app.posts.services import PostsServices
from app.comments.schemas import (
    CommentDataRequestSchema,
    CommentDeleteRequestSchema,
    CommentDataResponseSchema,
    MappedCommentDataResponseSchema
)


router = APIRouter(
    prefix="/comments",
    tags=["Comments"],
)


@router.get("/my-comments")
async def get_list_of_my_comments(
        user=GetCurrentUser,
        comments_services: CommentsServices = GetCommentsService
) -> List[CommentDataResponseSchema]:
    return await comments_services.get_my_comments(user_id=user.id)


@router.get("/post-comments/{post_id}")
async def get_list_of_comments_by_post_id(
        post_id: int,
        comments_services: CommentsServices = GetCommentsService
) -> List[CommentDataResponseSchema]:
    return await comments_services.get_list_comments_by_post_id(post_id=post_id)


@router.post("/create")
async def create_comment(
        comment_data: CommentDataRequestSchema,
        user=GetCurrentUser,
        comments_services: CommentsServices = GetCommentsService,
        post_services: PostsServices = GetPostsService
) -> MappedCommentDataResponseSchema:
    await post_services.check_permission(post_id=comment_data.post_id, black_list=user.im_blacklisted)
    return await comments_services.create_comment(
        user_id=user.id,
        post_id=comment_data.post_id,
        text=comment_data.text
    )


@router.delete("/delete")
async def delete_comment(
        comment_data: CommentDeleteRequestSchema,
        user=GetCurrentUser,
        comments_services: CommentsServices = GetCommentsService,
):
    return await comments_services.delete_comment(user_id=user.id, comment_id=comment_data.comment_id)
