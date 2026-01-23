from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.interaction import Interaction
from app.schemas.interaction import InteractionCreate, InteractionOut

router = APIRouter(prefix="/interactions", tags=["interactions"])


@router.post("", response_model=InteractionOut)
def create_interaction(payload: InteractionCreate, db: Session = Depends(get_db)):
    interaction = Interaction(**payload.model_dump())
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    return interaction


@router.get("", response_model=list[InteractionOut])
def list_interactions(
    customer_id: int | None = Query(None),
    policy_id: int | None = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(Interaction).order_by(Interaction.id.desc())

    if customer_id is not None:
        q = q.filter(Interaction.customer_id == customer_id)
    if policy_id is not None:
        q = q.filter(Interaction.policy_id == policy_id)

    return q.all()
