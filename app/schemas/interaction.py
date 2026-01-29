from datetime import datetime
from pydantic import BaseModel
from typing import Literal

Channel = Literal["call", "sms", "email", "note"]
Direction = Literal["outbound", "inbound"]


class InteractionCreate(BaseModel):
    customer_id: int
    policy_id: int | None = None
    channel: Channel
    direction: Direction = "outbound"
    subject: str | None = None
    body: str


class InteractionOut(BaseModel):
    id: int
    agency_id: int
    customer_id: int
    policy_id: int | None
    channel: str
    direction: str
    subject: str | None
    body: str
    created_at: datetime

    model_config = {"from_attributes": True}
