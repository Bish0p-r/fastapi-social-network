from enum import Enum

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Enum as EnumField, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base
from app.blacklist.models import Blacklist
from app.posts.models import Posts
from app.likes.models import Like


class PrivacySettingsEnum(str, Enum):
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

    posts = relationship('Posts', back_populates='author')

    liked_posts = relationship('Like', back_populates='user')
