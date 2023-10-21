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


class MappingPostSchema(BaseModel):
    Posts: PostDataResponseSchema


class PostAuthorIDRequestSchema(BaseModel):
    id: int


class PostUpdateRequestSchema(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
