from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PostDataRequestSchema(BaseModel):
    title: str | None
    content: str


class PostIDRequestSchema(BaseModel):
    id: int


class PostDataResponseSchema(BaseModel):
    id: int
    author_id: int
    title: str | None
    content: str
    created_at: datetime
    updated_at: datetime
    likes_count: int | None = None


class MappingPostSchema(BaseModel):
    Posts: PostDataResponseSchema


class PostAuthorIDRequestSchema(BaseModel):
    id: int


class PostUpdateRequestSchema(BaseModel):
    title: str = None
    content: str = None
