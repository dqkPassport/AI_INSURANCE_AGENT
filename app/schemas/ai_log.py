from pydantic import BaseModel


class AiLogOut(BaseModel):
    id: int
    policy_id: int | None
    template_name: str | None
    tone: str
    channel: str
    validation_passed: bool
    validation_error: str | None

    model_config = {"from_attributes": True}
