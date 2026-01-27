from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerOut
from app.core.tenant import get_agency_id
from app.core.auth_deps import get_current_agency_id

router = APIRouter(prefix="/customers", tags=["customers"])


@router.post("", response_model=CustomerOut)
def create_customer(
    payload: CustomerCreate,
    db: Session = Depends(get_db),
    agency_id: int = Depends(get_current_agency_id),
):
    customer = Customer(agency_id=agency_id, **payload.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


@router.get("", response_model=list[CustomerOut])
def list_customers(
    db: Session = Depends(get_db),
    agency_id: int = Depends(get_current_agency_id),
):
    return (
        db.query(Customer)
        .filter(Customer.agency_id == agency_id)
        .order_by(Customer.id.desc())
        .all()
    )
