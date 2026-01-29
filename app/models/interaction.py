from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from app.db.base import Base


class Interaction(Base):
    __tablename__ = "interactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    agency_id: Mapped[int] = mapped_column(ForeignKey("agencies.id"), index=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), index=True)
    policy_id: Mapped[int | None] = mapped_column(
        ForeignKey("policies.id"), nullable=True, index=True
    )

    channel: Mapped[str] = mapped_column(String(20))  # call/sms/email/note
    direction: Mapped[str] = mapped_column(
        String(20), default="outbound"
    )  # outbound/inbound
    subject: Mapped[str | None] = mapped_column(String(200), nullable=True)
    body: Mapped[str] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, index=True
    )

    customer = relationship("Customer", back_populates="interactions")
    policy = relationship("Policy", back_populates="interactions")
