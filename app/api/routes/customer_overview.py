from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.api.deps import get_db
from app.models.customer import Customer
from app.models.policy import Policy
from app.models.task import Task
from app.models.interaction import Interaction
from app.schemas.overview import CustomerOverviewOut

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("/{customer_id}/overview", response_model=CustomerOverviewOut)
def get_customer_overview(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    policies_count = (
        db.query(func.count(Policy.id))
        .filter(Policy.customer_id == customer_id)
        .scalar()
        or 0
    )

    interactions_count = (
        db.query(func.count(Interaction.id))
        .filter(Interaction.customer_id == customer_id)
        .scalar()
        or 0
    )

    open_tasks_count = (
        db.query(func.count(Task.id))
        .filter(Task.customer_id == customer_id, Task.status == "open")
        .scalar()
        or 0
    )

    nearest_expiration_date = (
        db.query(func.min(Policy.expiration_date))
        .filter(Policy.customer_id == customer_id)
        .scalar()
    )

    return CustomerOverviewOut(
        id=customer.id,
        full_name=customer.full_name,
        email=customer.email,
        phone=customer.phone,
        policies_count=policies_count,
        interactions_count=interactions_count,
        open_tasks_count=open_tasks_count,
        nearest_expiration_date=nearest_expiration_date,
    )
