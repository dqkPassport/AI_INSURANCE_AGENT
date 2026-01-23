from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

from sqlalchemy.orm import Session, joinedload

from app.models.policy import Policy


@dataclass
class RenewalItem:
    policy: Policy
    days_to_expire: int
    increase_amount: float | None
    increase_pct: float | None
    is_shock: bool


def _calc_increase(old_premium: float, renewal_premium: float | None) -> tuple[float | None, float | None]:
    """
    Returns (increase_amount, increase_pct).
    If renewal_premium is None, returns (None, None).
    """
    if renewal_premium is None:
        return None, None

    increase_amount = renewal_premium - old_premium

    # avoid divide-by-zero
    if old_premium <= 0:
        return increase_amount, None

    increase_pct = increase_amount / old_premium
    return increase_amount, increase_pct


def get_renewals(db: Session, *, days: int, shock_threshold: float) -> list[RenewalItem]:
    """
    Get policies expiring within the next `days`.
    Adds computed fields:
      - days_to_expire
      - increase amount / percent
      - shock flag
    """
    today = date.today()
    end_date = today + timedelta(days=days)

    policies = (
        db.query(Policy)
        .options(joinedload(Policy.customer))
        .filter(Policy.expiration_date >= today, Policy.expiration_date <= end_date)
        .order_by(Policy.expiration_date.asc())
        .all()
    )

    results: list[RenewalItem] = []
    for p in policies:
        days_to_expire = (p.expiration_date - today).days
        inc_amount, inc_pct = _calc_increase(p.old_premium, p.renewal_premium)

        is_shock = (inc_pct is not None) and (inc_pct >= shock_threshold)

        results.append(
            RenewalItem(
                policy=p,
                days_to_expire=days_to_expire,
                increase_amount=inc_amount,
                increase_pct=inc_pct,
                is_shock=is_shock,
            )
        )

    return results
