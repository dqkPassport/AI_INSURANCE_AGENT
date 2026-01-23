from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.policy import Policy
from app.schemas.policy import PolicyCreate, PolicyOut

router = APIRouter(prefix="/policies", tags=["policies"])


@router.post("", response_model=PolicyOut)
def create_policy(payload: PolicyCreate, db: Session = Depends(get_db)):
    policy = Policy(**payload.model_dump())
    db.add(policy)
    db.commit()
    db.refresh(policy)
    return policy


@router.get("", response_model=list[PolicyOut])
def list_policies(db: Session = Depends(get_db)):
    return db.query(Policy).order_by(Policy.id.desc()).all()
