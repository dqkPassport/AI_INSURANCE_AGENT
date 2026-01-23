from datetime import date
from pydantic import BaseModel


class CustomerOverviewOut(BaseModel):
    id: int
    full_name: str
    email: str | None
    phone: str | None

    policies_count: int
    interactions_count: int
    open_tasks_count: int

    nearest_expiration_date: date | None

    model_config = {"from_attributes": True}
