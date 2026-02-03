from datetime import date
from pydantic import BaseModel
from pydantic import BaseModel, field_validator


class PolicyCreate(BaseModel):
    customer_id: int
    policy_number: str
    carrier: str
    product_type: str
    effective_date: date
    expiration_date: date
    old_premium: float
    renewal_premium: float

    @field_validator("renewal_premium")
    @classmethod
    def premium_non_negative(cls, v: float):
        if v < 0:
            raise ValueError("renewal_premium must be 0 or higher")
        return v

    @field_validator("expiration_date")
    @classmethod
    def expiration_after_effective(cls, expiration_date: date, info):
        effective_date = info.data.get("effective_date")
        if effective_date and expiration_date <= effective_date:
            raise ValueError("expiration_date must be after effective_date")
        return expiration_date

    @field_validator("old_premium")
    @classmethod
    def old_premium_non_negative(cls, v: float):
        if v < 0:
            raise ValueError("old_premium must be 0 or higher")
        return v


class PolicyOut(BaseModel):
    id: int
    agency_id: int
    customer_id: int
    policy_number: str
    carrier: str
    product_type: str
    effective_date: date
    expiration_date: date
    old_premium: float
    renewal_premium: float | None

    model_config = {"from_attributes": True}
