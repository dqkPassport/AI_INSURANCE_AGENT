from datetime import date, datetime
from sqlalchemy import String, Date, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)

    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), index=True)
    policy_id: Mapped[int | None] = mapped_column(
        ForeignKey("policies.id"), nullable=True, index=True
    )

    title: Mapped[str] = mapped_column(String(200))
    due_date: Mapped[date] = mapped_column(Date, index=True)
    status: Mapped[str] = mapped_column(String(20), default="open")  # open/done
    priority: Mapped[str] = mapped_column(
        String(10), default="normal"
    )  # low/normal/high

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="tasks")
    policy = relationship("Policy", back_populates="tasks")
