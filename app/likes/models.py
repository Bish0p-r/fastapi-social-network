from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base


if TYPE_CHECKING:
    from app.users.models import Users
    from app.posts.models import Posts


class Like(Base):
    __tablename__ = 'likes'
    __table_args__ = (UniqueConstraint('user_id', 'post_id'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'))

    user: Mapped['Users'] = relationship(back_populates='liked_posts')
    post: Mapped['Posts'] = relationship(back_populates='liked_by')

    def __str__(self):
        return f"LikeID: {self.id}, UserID: {self.user_id}, PostID: {self.post_id}"
