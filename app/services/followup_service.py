from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.models.policy import Policy
from app.models.task import Task


def _task_exists(db: Session, *, policy_id: int, title: str, due_date: date) -> bool:
    return (
        db.query(Task)
        .filter(
            Task.policy_id == policy_id,
            Task.title == title,
            Task.due_date == due_date,
            Task.status == "open",
        )
        .first()
        is not None
    )


def create_renewal_followup_plan(db: Session, *, policy: Policy) -> list[Task]:
    """
    Creates a simple 3-step follow-up plan for a renewal.
    Idempotent-ish: won't create duplicates if same open task already exists.
    """
    today = date.today()

    # Basic cadence (you can change later per agency)
    plan = [
        ("Send renewal text/email (friendly check-in)", today),
        ("Call customer about renewal options", today + timedelta(days=2)),
        ("Final follow-up before expiration", today + timedelta(days=5)),
    ]

    created: list[Task] = []
    for title, due in plan:
        # Don’t schedule tasks after expiration
        if due > policy.expiration_date:
            continue

        if _task_exists(db, policy_id=policy.id, title=title, due_date=due):
            continue

        t = Task(
            customer_id=policy.customer_id,
            policy_id=policy.id,
            title=title,
            due_date=due,
            status="open",
        )
        db.add(t)
        created.append(t)

    db.commit()
    for t in created:
        db.refresh(t)

    return created
