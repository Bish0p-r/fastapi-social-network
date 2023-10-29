from enum import Enum
from datetime import date
from typing import TYPE_CHECKING, List

from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.database import Base


if TYPE_CHECKING:
    from app.blacklist.models import Blacklist
    from app.posts.models import Posts
    from app.likes.models import Like
    from app.comments.models import Comment
    from app.friendships.models import Friendships


class PrivacySettingsEnum(str, Enum):
    PUBLIC = "public"
    FRIENDS = "friends"
    PRIVATE = "private"


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    date_of_birth: Mapped[date] = mapped_column(nullable=True)
    bio: Mapped[str] = mapped_column(nullable=True)
    privacy_settings: Mapped[PrivacySettingsEnum] = mapped_column(default=PrivacySettingsEnum.PUBLIC)

    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=False)

    incoming_requests: Mapped[List["Friendships"]] = relationship(foreign_keys="[Friendships.to_user]")
    outgoing_requests: Mapped[List["Friendships"]] = relationship(foreign_keys="[Friendships.from_user]")

    my_blacklist: Mapped[List["Blacklist"]] = relationship(foreign_keys="[Blacklist.initiator_user]")
    im_blacklisted: Mapped[List["Blacklist"]] = relationship(foreign_keys="[Blacklist.blocked_user]")

    posts: Mapped[List["Posts"]] = relationship(back_populates="author")

    liked_posts: Mapped[List["Like"]] = relationship(back_populates="user")

    commented_posts: Mapped[List["Comment"]] = relationship(back_populates="user")

    def __str__(self):
        return f"User #{self.id}, Email: {self.email}"
