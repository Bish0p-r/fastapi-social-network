from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PostDataRequestSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

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
    model_config = ConfigDict(extra="forbid")

    title: str = None
    content: str = None
