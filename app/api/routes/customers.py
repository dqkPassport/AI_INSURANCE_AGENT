from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerOut

router = APIRouter(prefix="/customers", tags=["customers"])


@router.post("", response_model=CustomerOut)
def create_customer(payload: CustomerCreate, db: Session = Depends(get_db)):
    customer = Customer(**payload.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


@router.get("", response_model=list[CustomerOut])
def list_customers(db: Session = Depends(get_db)):
    return db.query(Customer).order_by(Customer.id.desc()).all()
