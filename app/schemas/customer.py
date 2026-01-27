from pydantic import BaseModel


class CustomerCreate(BaseModel):
    full_name: str
    email: str | None = None
    phone: str | None = None


class CustomerOut(BaseModel):
    id: int
    agency_id: int
    full_name: str
    email: str | None
    phone: str | None

    model_config = {"from_attributes": True}
