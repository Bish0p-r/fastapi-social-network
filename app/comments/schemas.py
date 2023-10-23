from datetime import datetime

from pydantic import BaseModel


class CommentDataRequestSchema(BaseModel):
    post_id: int
    text: str


class CommentDeleteRequestSchema(BaseModel):
    comment_id: int


class CommentDataResponseSchema(BaseModel):
    id: int
    user_id: int
    post_id: int
    text: str
    created_at: datetime
    updated_at: datetime


class MappedCommentDataResponseSchema(BaseModel):
    Comment: CommentDataResponseSchema
