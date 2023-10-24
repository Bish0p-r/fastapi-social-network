from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Enum as EnumField, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base


class Friendships(Base):
    __tablename__ = 'friendships'
    __table_args__ = (UniqueConstraint('to_user', 'from_user'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    to_user: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    from_user: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    is_accepted: Mapped[bool] = mapped_column(default=False)

    # incoming_requests = relationship(
    #     'Users',
    #     foreign_keys="[Friendships.to_user]",
    #     back_populates='incoming_requests'
    # )
    # outgoing_requests = relationship(
    #     'Users',
    #     foreign_keys="[Friendships.from_user]",
    #     back_populates='outgoing_requests'
    # )
