from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.policy import Policy


def get_customer_or_404(db: Session, agency_id: int, customer_id: int) -> Customer:
    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .filter(Customer.agency_id == agency_id)
        .first()
    )
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


def get_policy_or_404(db: Session, agency_id: int, policy_id: int) -> Policy:
    policy = (
        db.query(Policy)
        .filter(Policy.id == policy_id)
        .filter(Policy.agency_id == agency_id)
        .first()
    )
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return policy
