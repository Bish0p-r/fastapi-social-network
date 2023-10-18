from datetime import date
from enum import Enum
from pydantic import BaseModel, EmailStr
from app.users.models import PrivacySettingsEnum


class UserSchema(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    privacy_settings: PrivacySettingsEnum
    date_of_birth: date | None
    bio: str | None
    is_active: bool


class UserMappingSchema(BaseModel):
    Users: UserSchema


class FriendshipSchema(BaseModel):
    id: int
    to_user: int
    from_user: int
    is_accepted: bool


class MappingFriendShipSchema(BaseModel):
    Friendships: FriendshipSchema


class FriendShipRequestSchema(BaseModel):
    to_user: int
