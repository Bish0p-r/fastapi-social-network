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
