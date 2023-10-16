from pydantic import BaseModel


class UserProfileSchema(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    age: int
    bio: str