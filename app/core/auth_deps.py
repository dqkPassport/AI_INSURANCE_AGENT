from fastapi import Header, HTTPException
import jwt
from jwt import InvalidTokenError
from app.core.settings import settings


def get_current_agency_id(authorization: str | None = Header(None)) -> int:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")
    token = authorization.split(" ", 1)[1].strip()
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_alg])
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    agency_id = payload.get("agency_id")
    if not agency_id:
        raise HTTPException(status_code=401, detail="Token missing agency_id")
    return int(agency_id)
