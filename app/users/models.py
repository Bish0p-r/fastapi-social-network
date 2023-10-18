from enum import Enum

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Enum as EnumField
from sqlalchemy.orm import relationship

from app.database import Base


class PrivacySettingsEnum(Enum):
    PUBLIC = 'public'
    FRIENDS = 'friends'
    PRIVATE = 'private'


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date)
    bio = Column(String)
    privacy_settings = Column(EnumField(PrivacySettingsEnum), default=PrivacySettingsEnum.PUBLIC)

    is_superuser = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)

    incoming_requests = relationship('Friendships', foreign_keys="[Friendships.to_user]")
    outgoing_requests = relationship('Friendships', foreign_keys="[Friendships.from_user]")


class Friendships(Base):
    __tablename__ = 'friendships'

    id = Column(Integer, primary_key=True)
    to_user = Column(Integer, ForeignKey('users.id'))
    from_user = Column(Integer, ForeignKey('users.id'))

    is_accepted = Column(Boolean, default=False)

    incoming_requests = relationship(
        'Users',
        foreign_keys="[Friendships.to_user]",
        back_populates='incoming_requests'
    )
    outgoing_requests = relationship(
        'Users',
        foreign_keys="[Friendships.from_user]",
        back_populates='outgoing_requests'
    )
