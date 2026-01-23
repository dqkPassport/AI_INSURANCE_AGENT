from datetime import datetime

from sqlalchemy import String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AiRewriteLog(Base):
    __tablename__ = "ai_rewrite_logs"

    id: Mapped[int] = mapped_column(primary_key=True)

    policy_id: Mapped[int | None] = mapped_column(nullable=True, index=True)
    template_name: Mapped[str | None] = mapped_column(String(80), nullable=True)

    tone: Mapped[str] = mapped_column(String(30))
    channel: Mapped[str] = mapped_column(String(20))

    base_text: Mapped[str] = mapped_column(Text)
    rewritten_text: Mapped[str] = mapped_column(Text)

    validation_passed: Mapped[bool] = mapped_column(default=True)
    validation_error: Mapped[str | None] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
