from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.auth_deps import get_current_agency_id

from app.models.customer import Customer
from app.models.policy import Policy
from app.models.task import Task
from app.models.interaction import Interaction
from app.schemas.dashboard import DashboardSummaryOut

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummaryOut)
def get_dashboard_summary(
    db: Session = Depends(get_db),
    agency_id: int = Depends(get_current_agency_id),
):
    today = date.today()
    next_30 = today + timedelta(days=30)
    next_7 = today + timedelta(days=7)

    # interactions.created_at is DATETIME in your app.db,
    # so we filter with datetime (not date).
    last_7_dt = datetime.utcnow() - timedelta(days=7)

    customers_total = (
        db.query(func.count(Customer.id))
        .filter(Customer.agency_id == agency_id)
        .scalar()
    )

    policies_total = (
        db.query(func.count(Policy.id)).filter(Policy.agency_id == agency_id).scalar()
    )

    # Your DB uses policies.expiration_date (DATE)
    policies_expiring_30_days = (
        db.query(func.count(Policy.id))
        .filter(Policy.agency_id == agency_id)
        .filter(Policy.expiration_date >= today)
        .filter(Policy.expiration_date <= next_30)
        .scalar()
    )

    open_tasks_total = (
        db.query(func.count(Task.id))
        .filter(Task.agency_id == agency_id)
        .filter(Task.status == "open")
        .scalar()
    )

    # Your DB uses interactions.created_at (DATETIME)
    interactions_last_7_days = (
        db.query(func.count(Interaction.id))
        .filter(Interaction.agency_id == agency_id)
        .filter(Interaction.created_at >= last_7_dt)
        .scalar()
    )

    tasks_due_next_7_days = (
        db.query(func.count(Task.id))
        .filter(Task.agency_id == agency_id)
        .filter(Task.status == "open")
        .filter(Task.due_date >= today)
        .filter(Task.due_date <= next_7)
        .scalar()
    )

    return DashboardSummaryOut(
        customers_total=customers_total or 0,
        policies_total=policies_total or 0,
        policies_expiring_30_days=policies_expiring_30_days or 0,
        open_tasks_total=open_tasks_total or 0,
        interactions_last_7_days=interactions_last_7_days or 0,
        tasks_due_next_7_days=tasks_due_next_7_days or 0,
        today=today,
    )
