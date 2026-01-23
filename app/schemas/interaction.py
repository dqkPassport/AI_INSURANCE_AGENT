from pydantic import BaseModel


class InteractionCreate(BaseModel):
    customer_id: int
    policy_id: int | None = None
    channel: str  # phone/text/email/chat
    direction: str  # inbound/outbound
    content: str


class InteractionOut(BaseModel):
    id: int
    customer_id: int
    policy_id: int | None
    channel: str
    direction: str
    content: str

    model_config = {"from_attributes": True}
