# app/services/interactions_service.py
from sqlalchemy.orm import Session
from app.models.customer import Customer
from app.models.interaction import Interaction


def create_interaction(
    db: Session,
    *,
    agency_id: int,
    customer_id: int,
    channel: str,
    subject: str | None,
    body: str | None,
    created_by_user_id: int | None,
) -> Interaction:
    # Security: confirm customer belongs to this agency
    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id, Customer.agency_id == agency_id)
        .first()
    )
    if not customer:
        raise ValueError("Customer not found")

    interaction = Interaction(
        agency_id=agency_id,
        customer_id=customer_id,
        channel=channel,
        subject=subject,
        body=body,
        created_by_user_id=created_by_user_id,
    )
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    return interaction
