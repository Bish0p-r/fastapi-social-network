from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, String, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base


if TYPE_CHECKING:
    from app.users.models import Users
    from app.posts.models import Posts


class Comment(Base):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(512))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'))

    user: Mapped['Users'] = relationship(back_populates='commented_posts')
    post: Mapped['Posts'] = relationship(back_populates='comments')

    def __str__(self):
        return f"CommentID: {self.id}, UserID: {self.user_id}, PostID: {self.post_id}"
