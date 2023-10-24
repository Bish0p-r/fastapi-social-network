from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base


if TYPE_CHECKING:
    from app.users.models import Users
    from app.likes.models import Like
    from app.comments.models import Comment


class Posts(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(64), nullable=True)
    content: Mapped[str] = mapped_column(String(1024))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    author: Mapped['Users'] = relationship(back_populates='posts')

    liked_by: Mapped[List['Like']] = relationship(back_populates='post')

    comments: Mapped[List['Comment']] = relationship(back_populates='post')
