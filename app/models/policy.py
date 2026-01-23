from datetime import date, datetime
from sqlalchemy import String, Date, DateTime, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Policy(Base):
    __tablename__ = "policies"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), index=True)

    policy_number: Mapped[str] = mapped_column(String(60), index=True)
    carrier: Mapped[str] = mapped_column(String(80))
    product_type: Mapped[str] = mapped_column(String(80))  # auto/home/life/etc

    effective_date: Mapped[date] = mapped_column(Date)
    expiration_date: Mapped[date] = mapped_column(Date, index=True)

    old_premium: Mapped[float] = mapped_column(Float)          # last term premium
    renewal_premium: Mapped[float | None] = mapped_column(Float, nullable=True)  # new quote

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="policies")
    interactions = relationship("Interaction", back_populates="policy", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="policy", cascade="all, delete-orphan")
