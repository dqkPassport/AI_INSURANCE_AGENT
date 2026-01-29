from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.auth_deps import get_current_agency_id
from app.models.customer import Customer
from app.models.interaction import Interaction
from app.models.task import Task

router = APIRouter(prefix="/timeline", tags=["timeline"])


@router.get("/customer/{customer_id}")
def customer_timeline(
    customer_id: int,
    db: Session = Depends(get_db),
    agency_id: int = Depends(get_current_agency_id),
):
    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id, Customer.agency_id == agency_id)
        .first()
    )
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    interactions = (
        db.query(Interaction)
        .filter(
            Interaction.agency_id == agency_id,
            Interaction.customer_id == customer_id,
        )
        .all()
    )

    tasks = (
        db.query(Task)
        .filter(
            Task.agency_id == agency_id,
            Task.customer_id == customer_id,
        )
        .all()
    )

    items = []

    for i in interactions:
        items.append(
            {
                "type": "interaction",
                "id": i.id,
                "ts": i.created_at,
                "channel": i.channel,
                "direction": i.direction,
                "subject": i.subject,
                "body": i.body,
            }
        )

    for t in tasks:
        # if your Task has created_at use it; otherwise use due_date as a “timeline time”
        ts = getattr(t, "created_at", None) or datetime.combine(
            t.due_date, datetime.min.time()
        )
        items.append(
            {
                "type": "task",
                "id": t.id,
                "ts": ts,
                "title": t.title,
                "status": t.status,
                "priority": getattr(t, "priority", "normal"),
                "due_date": t.due_date,
            }
        )

    items.sort(key=lambda x: x["ts"], reverse=True)
    return {"customer_id": customer_id, "items": items}
