from datetime import date
from typing import List

from pydantic import BaseModel, EmailStr, model_validator, field_validator
from app.users.models import PrivacySettingsEnum
from app.friendships.schemas import FriendshipSchema
from app.blacklist.schemas import BlackListSchema
from app.comments.schemas import CommentDataResponseSchema
from app.likes.schemas import LikeSchema
from app.posts.schemas import PostDataResponseSchema


class UserSchema(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    privacy_settings: PrivacySettingsEnum
    date_of_birth: date | None
    bio: str | None
    is_active: bool


class UserFullInfoSchema(UserSchema):
    posts: List[PostDataResponseSchema]
    liked_posts: List[LikeSchema]
    commented_posts: List[CommentDataResponseSchema]
    outgoing_requests: List[FriendshipSchema]
    incoming_requests: List[FriendshipSchema]
    my_blacklist: List[BlackListSchema]
    im_blacklisted: List[BlackListSchema]


class UserMappingSchema(BaseModel):
    Users: UserSchema


class UserDetailsSchema(UserSchema):
    im_blacklisted: list | None


class UserUpdateSchema(BaseModel):
    first_name: str = None
    last_name: str = None
    privacy_settings: PrivacySettingsEnum = PrivacySettingsEnum.PUBLIC
    date_of_birth: date = None
    bio: str | None = None

    @model_validator(mode="before")
    @classmethod
    def validate_privacy_settings(cls, value):
        settings_value = value.get("privacy_settings")
        if settings_value is None:
            value["privacy_settings"] = PrivacySettingsEnum.PUBLIC
            return value
        if settings_value not in [PrivacySettingsEnum.PUBLIC, PrivacySettingsEnum.FRIENDS, PrivacySettingsEnum.PRIVATE]:
            raise ValueError("Privacy settings must be one of PUBLIC, FRIENDS or PRIVATE")
        return value
