from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import verify_password, create_access_token
from app.core.settings import settings
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenOut
from app.schemas.auth import RegisterRequest, UserOut

from app.core.security import hash_password
from app.core.auth_deps import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenOut)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        sub=str(user.id),
        agency_id=user.agency_id,
        expires_minutes=settings.access_token_expire_minutes,
    )
    return TokenOut(access_token=token)


@router.post("/register", response_model=UserOut)
def register_user(
    payload: RegisterRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    exists = db.query(User).filter(User.email == payload.email).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email already exists")

    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        agency_id=payload.agency_id,
        role=payload.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
