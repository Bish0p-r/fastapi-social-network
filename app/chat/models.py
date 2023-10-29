from datetime import datetime

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(1024))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    from_user: Mapped[int] = mapped_column(ForeignKey("users.id"))
    to_user: Mapped[int] = mapped_column(ForeignKey("users.id"))

    def __str__(self):
        return f"MessageID: {self.id}, FromUser: {self.from_user}, ToUser: {self.to_user}"
