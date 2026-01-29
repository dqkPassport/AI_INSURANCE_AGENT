# app/schemas/timeline.py
from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime

TimelineItemType = Literal["interaction", "task"]


class TimelineItem(BaseModel):
    type: TimelineItemType
    id: int
    customer_id: int
    timestamp: datetime

    # common fields (optional depending on type)
    title: Optional[str] = None
    details: Optional[str] = None
    channel: Optional[str] = None
    status: Optional[str] = None
