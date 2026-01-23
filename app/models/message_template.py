from datetime import datetime

from sqlalchemy import String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class MessageTemplate(Base):
    __tablename__ = "message_templates"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(80), unique=True, index=True
    )  # e.g. "renewal_sms_friendly"
    channel: Mapped[str] = mapped_column(String(20))  # sms/email
    body: Mapped[str] = mapped_column(Text)  # template text with {placeholders}

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
