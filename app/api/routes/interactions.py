from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.auth_deps import get_current_agency_id
from app.models.customer import Customer
from app.models.interaction import Interaction
from app.schemas.interaction import InteractionCreate, InteractionOut

router = APIRouter(prefix="/interactions", tags=["interactions"])


@router.post("", response_model=InteractionOut)
def create_interaction(
    payload: InteractionCreate,
    db: Session = Depends(get_db),
    agency_id: int = Depends(get_current_agency_id),
):
    # ✅ customer must belong to this agency
    customer = (
        db.query(Customer)
        .filter(Customer.id == payload.customer_id, Customer.agency_id == agency_id)
        .first()
    )
    if not customer:
        raise HTTPException(
            status_code=400, detail="Customer not found for this agency"
        )

    interaction = Interaction(agency_id=agency_id, **payload.model_dump())
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    return interaction


@router.get("", response_model=list[InteractionOut])
def list_interactions(
    customer_id: int | None = None,
    db: Session = Depends(get_db),
    agency_id: int = Depends(get_current_agency_id),
):
    q = db.query(Interaction).filter(Interaction.agency_id == agency_id)
    if customer_id is not None:
        q = q.filter(Interaction.customer_id == customer_id)
    return q.order_by(Interaction.created_at.desc()).all()
