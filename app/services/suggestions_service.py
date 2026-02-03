from __future__ import annotations

from datetime import date
from typing import List

from app.schemas.ai_suggestions import SuggestionOut


def pct_change(old: float, new: float) -> float:
    if old <= 0:
        return 0.0
    return ((new - old) / old) * 100.0


def build_policy_suggestions(
    *,
    expiration_date: date,
    old_premium: float,
    renewal_premium: float,
) -> List[SuggestionOut]:
    """
    Pure rules engine: it doesn't know the DB, just facts.
    This makes it easy to test.
    """
    suggestions: list[SuggestionOut] = []

    today = date.today()
    days_left = (expiration_date - today).days
    change_pct = pct_change(old_premium, renewal_premium)

    if days_left <= 3:
        suggestions.append(
            SuggestionOut(
                type="call",
                title="Call now (expires within 3 days)",
                reason=f"Policy expires in {days_left} day(s). Very urgent.",
                priority=1,
            )
        )
        suggestions.append(
            SuggestionOut(
                type="call",
                title="Call again tomorrow if no reply",
                reason="Two attempts reduces missed renewals.",
                priority=2,
            )
        )

    # Rule 1: Expiring soon -> act
    if days_left <= 7:
        suggestions.append(
            SuggestionOut(
                type="call",
                title="Call customer today (expires within 7 days)",
                reason=f"Policy expires in {days_left} day(s). Avoid a coverage lapse.",
                priority=1,
            )
        )
        suggestions.append(
            SuggestionOut(
                type="sms",
                title="Send urgent SMS reminder",
                reason="Short urgent message can get a fast response.",
                priority=2,
            )
        )

    # Rule 2: Medium urgency
    if 8 <= days_left <= 30:
        suggestions.append(
            SuggestionOut(
                type="sms",
                title="Send friendly renewal SMS",
                reason=f"Policy expires in {days_left} day(s). A quick reminder is helpful.",
                priority=3,
            )
        )

    # Rule 3: Price shock
    if change_pct >= 10:
        suggestions.append(
            SuggestionOut(
                type="call",
                title="Call customer (price shock)",
                reason=f"Renewal premium increased by {change_pct:.2f}%. Customers often want options.",
                priority=1,
            )
        )
        suggestions.append(
            SuggestionOut(
                type="note",
                title="Prepare options (shop market / adjust coverage)",
                reason="Offer alternatives: different carrier, deductible changes, coverage review.",
                priority=2,
            )
        )

    # Rule 4: Small change -> easy close
    if 0 <= change_pct < 10 and days_left <= 30:
        suggestions.append(
            SuggestionOut(
                type="email",
                title="Send renewal email with details",
                reason="Small change: many customers renew quickly with a clear email.",
                priority=4,
            )
        )

    # Rule 5: Always suggest creating a task for tracking
    if days_left <= 30:
        suggestions.append(
            SuggestionOut(
                type="task",
                title="Create follow-up task",
                reason="Tracking follow-ups prevents missed renewals.",
                priority=5,
            )
        )

    # Sort: priority ascending (1 first)
    suggestions.sort(key=lambda s: s.priority)
    return suggestions
