from pydantic import BaseModel


class TemplateCreate(BaseModel):
    name: str
    channel: str  # sms/email
    body: str


class TemplateOut(BaseModel):
    id: int
    name: str
    channel: str
    body: str

    model_config = {"from_attributes": True}
