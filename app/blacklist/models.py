from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


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
