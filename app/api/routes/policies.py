from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.policy import Policy
from app.schemas.policy import PolicyCreate, PolicyOut
from app.core.tenant import get_agency_id
from app.models.customer import Customer
from app.core.auth_deps import get_current_agency_id
from app.services.access_control import get_customer_or_404

router = APIRouter(prefix="/policies", tags=["policies"])


@router.post("", response_model=PolicyOut)
def create_policy(
    payload: PolicyCreate,
    db: Session = Depends(get_db),
    agency_id: int = Depends(get_current_agency_id),
):
    # 1) Verify customer exists and belongs to this agency
    customer = get_customer_or_404(
        db=Session, agency_id=agency_id, customer_id=payload.customer_id
    )
    # customer = (
    #     db.query(Customer)
    #     .filter(Customer.id == payload.customer_id, Customer.agency_id == agency_id)
    #     .first()
    # )
    # if not customer:
    #     raise HTTPException(
    #         status_code=400, detail="Customer not found for this agency"
    #     )

    # 2) Create policy inside this agency
    policy = Policy(
        agency_id=agency_id,
        customer_id=customer.id,
        **payload.model_dump(),
    )
    db.add(policy)
    db.commit()
    db.refresh(policy)
    return policy


@router.get("", response_model=list[PolicyOut])
def list_policies(
    db: Session = Depends(get_db),
    agency_id: int = Depends(get_current_agency_id),
):
    return (
        db.query(Policy)
        .filter(Policy.agency_id == agency_id)
        .order_by(Policy.id.desc())
        .all()
    )
