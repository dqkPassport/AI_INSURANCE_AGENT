from fastapi import Header, HTTPException


def get_agency_id(x_agency_id: int | None = Header(None)) -> int:
    if x_agency_id is None:
        raise HTTPException(status_code=400, detail="Missing X-Agency-Id header")
    return x_agency_id
