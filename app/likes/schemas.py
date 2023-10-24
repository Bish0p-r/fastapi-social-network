from pydantic import BaseModel


class LikeSchema(BaseModel):
    id: int
    user_id: int
    post_id: int
