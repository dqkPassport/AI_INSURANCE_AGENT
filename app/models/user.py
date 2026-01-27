from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    agency_id: Mapped[int] = mapped_column(ForeignKey("agencies.id"), index=True)

    email: Mapped[str] = mapped_column(String(160), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))

    role: Mapped[str] = mapped_column(String(30), default="agent")  # agent/admin
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
