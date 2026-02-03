from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


Tone = Literal["friendly", "neutral", "urgent", "super_friendly"]
Channel = Literal["sms", "email"]


class RenewalFacts(BaseModel):
    customer_name: str = Field(min_length=1)
    policy_number: str = Field(min_length=1)
    carrier: str = Field(min_length=1)
    product_type: str = Field(min_length=1)
    expiration_date: date
    old_premium: float = Field(ge=0)
    renewal_premium: float = Field(ge=0)


class DraftRenewalRequest(BaseModel):
    tone: Tone = "friendly"
    channel: Channel = "sms"
    facts: RenewalFacts


class DraftRenewalFromPolicyRequest(BaseModel):
    tone: Tone = "friendly"
    channel: Channel = "sms"
    strict: bool = True  # if True, we enforce that key facts appear in the output


class DraftRenewalOut(BaseModel):
    tone: Tone
    channel: Channel
    drafted_text: str
