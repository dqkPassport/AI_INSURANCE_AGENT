from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.agency import Agency
from app.schemas.agency import AgencyCreate, AgencyOut

router = APIRouter(prefix="/agencies", tags=["agencies"])


@router.post("", response_model=AgencyOut)
def create_agency(payload: AgencyCreate, db: Session = Depends(get_db)):
    exists = db.query(Agency).filter(Agency.name == payload.name).first()
    if exists:
        raise HTTPException(status_code=400, detail="Agency name already exists")

    a = Agency(name=payload.name)
    db.add(a)
    db.commit()
    db.refresh(a)
    return a


@router.get("", response_model=list[AgencyOut])
def list_agencies(db: Session = Depends(get_db)):
    return db.query(Agency).order_by(Agency.id.desc()).all()
