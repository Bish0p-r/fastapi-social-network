from enum import Enum

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Enum as EnumField
from sqlalchemy.orm import relationship

from app.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    is_superuser = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)

    friendships = relationship('Friendships', back_populates='users')
    profile = relationship('UserProfile', back_populates='user')


class Friendships(Base):
    __tablename__ = 'friendships'

    id = Column(Integer, primary_key=True)
    to_user = Column(Integer, ForeignKey('users.id'))
    from_user = Column(Integer, ForeignKey('users.id'))

    is_accepted = Column(Boolean, default=False)

    users = relationship('Users', back_populates='friendships')


class PrivacySettingsEnum(Enum):
    PUBLIC = 'public'
    FRIENDS = 'friends'
    PRIVATE = 'private'


class UserProfile(Base):
    __tablename__ = 'user_profile'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date_of_birth = Column(Date)
    bio = Column(String)

    privacy_settings = Column(EnumField(PrivacySettingsEnum), default=PrivacySettingsEnum.PUBLIC.value)

    user = relationship('Users', back_populates='profile')

