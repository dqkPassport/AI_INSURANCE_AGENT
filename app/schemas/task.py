from datetime import date
from pydantic import BaseModel


class TaskCreate(BaseModel):
    customer_id: int
    policy_id: int | None = None
    title: str
    due_date: date


class TaskOut(BaseModel):
    id: int
    customer_id: int
    policy_id: int | None
    title: str
    due_date: date
    status: str

    model_config = {"from_attributes": True}
