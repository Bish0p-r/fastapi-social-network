from pydantic import BaseModel


class UserIDRequestSchema(BaseModel):
    user_id: int
