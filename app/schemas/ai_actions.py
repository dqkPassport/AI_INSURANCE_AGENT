from typing import Literal

from pydantic import BaseModel, Field


SuggestionType = Literal["call", "sms", "email", "task", "note"]


class GenerateTasksRequest(BaseModel):
    include_types: list[SuggestionType] = Field(
        default_factory=lambda: ["call", "sms", "email"]
    )
    due_in_days: int = Field(default=1, ge=0, le=30)
    dry_run: bool = False  # if True, do not create tasks, only preview


class GeneratedTaskOut(BaseModel):
    title: str
    status: str
    priority: str
    customer_id: int
    policy_id: int | None = None


class GenerateTasksOut(BaseModel):
    policy_id: int
    created_count: int
    tasks: list[GeneratedTaskOut]
