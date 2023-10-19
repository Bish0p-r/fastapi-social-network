from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Enum as EnumField, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


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
