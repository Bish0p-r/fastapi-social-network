from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base


class Blacklist(Base):
    __tablename__ = 'blacklist'
    __table_args__ = (UniqueConstraint('initiator_user', 'blocked_user'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    initiator_user: Mapped[int] = mapped_column(ForeignKey('users.id'))
    blocked_user: Mapped[int] = mapped_column(ForeignKey('users.id'))

    def __str__(self):
        return f"BlacklistID: {self.id}, InitiatorUserID: {self.initiator_user}, BlockedUserID: {self.blocked_user}"
