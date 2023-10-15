from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    age = Column(Integer)
    bio = Column(String)

    is_superuser = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)

    friendships = relationship('Friendships', back_populates='users')


class Friendships(Base):
    __tablename__ = 'friendships'

    id = Column(Integer, primary_key=True)
    to_user = Column(Integer, ForeignKey('users.id'))
    from_user = Column(Integer, ForeignKey('users.id'))

    is_accepted = Column(Boolean, default=False)

    users = relationship('Users', back_populates='friendships')
