from pydantic import BaseModel


class RewriteRequest(BaseModel):
    text: str
    tone: str  # friendly / neutral / urgent
    channel: str = "sms"  # sms / email


class RewriteOut(BaseModel):
    tone: str
    channel: str
    rewritten_text: str


class RewriteFromPolicyRequest(BaseModel):
    policy_id: int
    template_name: str
    tone: str  # friendly / neutral / urgent
    channel: str = "sms"  # optional override


class RewriteFromPolicyOut(BaseModel):
    policy_id: int
    template_name: str
    tone: str
    channel: str
    base_draft: str
    rewritten_draft: str
    warning: str | None = None
