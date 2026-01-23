from datetime import date
from pydantic import BaseModel


class PolicyCreate(BaseModel):
    customer_id: int
    policy_number: str
    carrier: str
    product_type: str
    effective_date: date
    expiration_date: date
    old_premium: float
    renewal_premium: float | None = None


class PolicyOut(BaseModel):
    id: int
    customer_id: int
    policy_number: str
    carrier: str
    product_type: str
    effective_date: date
    expiration_date: date
    old_premium: float
    renewal_premium: float | None

    model_config = {"from_attributes": True}
