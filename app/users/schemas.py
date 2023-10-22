from datetime import date

from pydantic import BaseModel, EmailStr, model_validator, field_validator
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
