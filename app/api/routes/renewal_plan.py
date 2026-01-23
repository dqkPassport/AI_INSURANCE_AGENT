from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.policy import Policy
from app.schemas.task import TaskOut
from app.services.followup_service import create_renewal_followup_plan

router = APIRouter(prefix="/renewals", tags=["renewals"])


@router.post("/{policy_id}/plan", response_model=list[TaskOut])
def generate_plan(policy_id: int, db: Session = Depends(get_db)):
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")

    tasks = create_renewal_followup_plan(db, policy=policy)
    return tasks
