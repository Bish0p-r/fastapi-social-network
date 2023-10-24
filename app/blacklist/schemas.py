from pydantic import BaseModel


class UserIDRequestSchema(BaseModel):
    user_id: int


class BlackListSchema(BaseModel):
    id: int
    initiator_user: int
    blocked_user: int
