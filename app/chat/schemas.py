from datetime import datetime

from pydantic import BaseModel


class MessageSchema(BaseModel):
    id: int
    from_user: int
    to_user: int
    content: str
    created_at: datetime
