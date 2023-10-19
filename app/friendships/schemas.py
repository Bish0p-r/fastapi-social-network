from pydantic import BaseModel


class FriendshipSchema(BaseModel):
    id: int
    to_user: int
    from_user: int
    is_accepted: bool


class MappingFriendShipSchema(BaseModel):
    Friendships: FriendshipSchema


class FriendShipRequestSchema(BaseModel):
    to_user: int
