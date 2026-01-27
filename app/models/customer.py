from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    agency_id: Mapped[int] = mapped_column(ForeignKey("agencies.id"), index=True)

    policies = relationship(
        "Policy", back_populates="customer", cascade="all, delete-orphan"
    )
    interactions = relationship(
        "Interaction", back_populates="customer", cascade="all, delete-orphan"
    )
    tasks = relationship(
        "Task", back_populates="customer", cascade="all, delete-orphan"
    )
    agency = relationship("Agency", back_populates="customers")
