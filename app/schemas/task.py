from datetime import date
from pydantic import BaseModel
from typing import Literal

priority = Literal["low", "normal", "high"]


class TaskCreate(BaseModel):
    customer_id: int
    policy_id: int | None = None
    title: str
    due_date: date
    priority: str = "normal"


class TaskOut(BaseModel):
    id: int
    customer_id: int
    policy_id: int | None
    title: str
    due_date: date
    status: str
    priority: str

    model_config = {"from_attributes": True}
