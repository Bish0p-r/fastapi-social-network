from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Friendships(Base):
    __tablename__ = "friendships"
    __table_args__ = (UniqueConstraint("to_user", "from_user"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    to_user: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    from_user: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    is_accepted: Mapped[bool] = mapped_column(default=False)

    def __str__(self):
        return f"FriendshipID: {self.id}, ToUserID: {self.to_user}, FromUserID: {self.from_user}"
