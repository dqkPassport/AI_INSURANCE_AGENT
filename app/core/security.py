from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt

from app.core.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def create_access_token(*, sub: str, agency_id: int, expires_minutes: int) -> str:
    now = datetime.utcnow()
    payload = {
        "sub": sub,
        "agency_id": agency_id,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=expires_minutes)).timestamp()),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_alg)
