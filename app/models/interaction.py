from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Interaction(Base):
    __tablename__ = "interactions"

    id: Mapped[int] = mapped_column(primary_key=True)

    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), index=True)
    policy_id: Mapped[int | None] = mapped_column(ForeignKey("policies.id"), nullable=True, index=True)

    channel: Mapped[str] = mapped_column(String(20))     # phone/text/email/chat
    direction: Mapped[str] = mapped_column(String(10))   # inbound/outbound
    content: Mapped[str] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="interactions")
    policy = relationship("Policy", back_populates="interactions")
