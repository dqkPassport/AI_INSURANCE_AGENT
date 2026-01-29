# app/services/timeline_service.py
from sqlalchemy.orm import Session
from app.models.customer import Customer
from app.models.interaction import Interaction
from app.models.task import Task  # assumes you already have Task model
from app.schemas.timeline import TimelineItem


def get_customer_timeline(
    db: Session, *, agency_id: int, customer_id: int
) -> list[TimelineItem]:
    # Security check: customer must belong to agency
    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id, Customer.agency_id == agency_id)
        .first()
    )
    if not customer:
        raise ValueError("Customer not found")

    interactions = (
        db.query(Interaction)
        .filter(
            Interaction.agency_id == agency_id, Interaction.customer_id == customer_id
        )
        .all()
    )

    tasks = (
        db.query(Task)
        .filter(Task.agency_id == agency_id, Task.customer_id == customer_id)
        .all()
    )

    items: list[TimelineItem] = []

    for i in interactions:
        items.append(
            TimelineItem(
                type="interaction",
                id=i.id,
                customer_id=i.customer_id,
                timestamp=i.created_at,
                title=i.subject,
                details=i.body,
                channel=i.channel,
            )
        )

    for t in tasks:
        # choose a timestamp: due_at if you have it, otherwise created_at
        ts = getattr(t, "due_at", None) or getattr(t, "created_at")
        items.append(
            TimelineItem(
                type="task",
                id=t.id,
                customer_id=t.customer_id,
                timestamp=ts,
                title=getattr(t, "title", None),
                details=getattr(t, "description", None),
                status=getattr(t, "status", None),
            )
        )

    # newest first
    items.sort(key=lambda x: x.timestamp, reverse=True)
    return items
