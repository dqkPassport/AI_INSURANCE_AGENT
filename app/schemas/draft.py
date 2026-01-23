from pydantic import BaseModel, Field


class DraftRenewalRequest(BaseModel):
    policy_id: int
    template_name: str


class DraftRenewalTonesRequest(BaseModel):
    policy_id: int
    template_names: list[str] = Field(min_length=3, max_length=3)


class DraftOut(BaseModel):
    template_name: str
    channel: str
    draft_text: str
