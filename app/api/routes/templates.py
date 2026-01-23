from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.message_template import MessageTemplate
from app.schemas.template import TemplateCreate, TemplateOut

router = APIRouter(prefix="/templates", tags=["templates"])


@router.post("", response_model=TemplateOut)
def create_template(payload: TemplateCreate, db: Session = Depends(get_db)):
    exists = (
        db.query(MessageTemplate).filter(MessageTemplate.name == payload.name).first()
    )
    if exists:
        raise HTTPException(status_code=400, detail="Template name already exists")

    t = MessageTemplate(**payload.model_dump())
    db.add(t)
    db.commit()
    db.refresh(t)
    return t


@router.get("", response_model=list[TemplateOut])
def list_templates(db: Session = Depends(get_db)):
    return db.query(MessageTemplate).order_by(MessageTemplate.id.desc()).all()


@router.get("/{template_id}", response_model=TemplateOut)
def get_template(template_id: int, db: Session = Depends(get_db)):
    t = db.query(MessageTemplate).filter(MessageTemplate.id == template_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Template not found")
    return t
