from datetime import date
from pydantic import BaseModel


class RenewalOut(BaseModel):
    policy_id: int
    customer_id: int
    customer_name: str

    policy_number: str
    carrier: str
    product_type: str
    effective_date: date
    expiration_date: date

    old_premium: float
    renewal_premium: float | None

    days_to_expire: int
    increase_amount: float | None
    increase_pct: float | None
    is_shock: bool

    model_config = {"from_attributes": True}
