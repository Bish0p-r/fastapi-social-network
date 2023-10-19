from enum import Enum

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Enum as EnumField, UniqueConstraint
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

    my_blacklist = relationship('Blacklist', foreign_keys="[Blacklist.initiator_user]")
    im_blacklisted = relationship('Blacklist', foreign_keys="[Blacklist.blocked_user]")


class Friendships(Base):
    __tablename__ = 'friendships'
    __table_args__ = (UniqueConstraint('to_user', 'from_user'),)

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


class Blacklist(Base):
    __tablename__ = 'blacklist'
    __table_args__ = (UniqueConstraint('initiator_user', 'blocked_user'),)

    id = Column(Integer, primary_key=True)
    initiator_user = Column(Integer, ForeignKey('users.id'))
    blocked_user = Column(Integer, ForeignKey('users.id'))

    my_blacklist = relationship(
        'Users',
        foreign_keys="[Blacklist.initiator_user]",
        back_populates='my_blacklist'
    )
    im_blacklisted = relationship(
        'Users',
        foreign_keys="[Blacklist.blocked_user]",
        back_populates='im_blacklisted'
    )
