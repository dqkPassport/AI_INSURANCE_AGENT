from typing import Literal
from pydantic import BaseModel


SuggestionType = Literal["call", "sms", "email", "task", "note"]


class SuggestionOut(BaseModel):
    type: SuggestionType
    title: str
    reason: str
    priority: int  # 1 (highest) -> 5 (lowest)


class SuggestionsResponse(BaseModel):
    policy_id: int
    suggestions: list[SuggestionOut]
