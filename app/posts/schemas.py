from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PostDataRequestSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None
    content: str


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


class PostUpdateRequestSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = None
    content: str = None
