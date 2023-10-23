from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, String, DateTime
from sqlalchemy.orm import relationship

from app.database import Base


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    text = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship('Users', back_populates='commented_posts')
    post = relationship('Posts', back_populates='comments')
