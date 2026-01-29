from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt

from app.core.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _truncate_bcrypt(password: str) -> str:
    b = password.encode("utf-8")
    if len(b) <= 72:
        return password
    # trim to 72 bytes safely (ignore partial utf-8 char)
    return b[:72].decode("utf-8", errors="ignore")


def hash_password(password: str) -> str:
    before = len(password.encode("utf-8"))
    password = _truncate_bcrypt(password)
    after = len(password.encode("utf-8"))
    print("hash_password bytes:", before, "->", after)
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    password = _truncate_bcrypt(password)
    return pwd_context.verify(password, hashed)


def create_access_token(*, sub: str, agency_id: int, expires_minutes: int) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": sub,
        "agency_id": agency_id,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=expires_minutes)).timestamp()),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_alg)
