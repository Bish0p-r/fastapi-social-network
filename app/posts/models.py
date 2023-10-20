from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base
from app.users.models import Users


class Posts(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'))

    author = relationship('Users', back_populates='posts')
