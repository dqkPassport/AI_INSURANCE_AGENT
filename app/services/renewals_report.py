from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Iterable

from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.policy import Policy


@dataclass
class RenewalReportRow:
    policy_id: int
    customer_id: int
    customer_name: str
    policy_number: str
    carrier: str
    product_type: str
    effective_date: date
    expiration_date: date
    days_until_expiration: int
    old_premium: float
    renewal_premium: float
    pct_change: float
    flag: str  # "OK" or "PRICE_SHOCK"


def _pct_change(old: float, new: float) -> float:
    if old is None or old == 0:
        return 0.0
    return ((new - old) / old) * 100.0


def build_renewals_report(
    db: Session,
    agency_id: int,
    days: int = 30,
    shock_threshold_pct: float = 10.0,
) -> list[RenewalReportRow]:
    today = date.today()
    until = today + timedelta(days=days)

    # Join Customer so we can export customer_name in the CSV.
    rows: Iterable[tuple[Policy, Customer]] = (
        db.query(Policy, Customer)
        .join(Customer, Customer.id == Policy.customer_id)
        .filter(Policy.agency_id == agency_id)
        .filter(Customer.agency_id == agency_id)
        .filter(Policy.expiration_date >= today)
        .filter(Policy.expiration_date <= until)
        .order_by(Policy.expiration_date.asc())
        .all()
    )

    report: list[RenewalReportRow] = []
    for policy, customer in rows:
        old_p = float(policy.old_premium or 0)
        new_p = float(policy.renewal_premium or 0)
        pct = _pct_change(old_p, new_p)
        flag = "PRICE_SHOCK" if pct >= shock_threshold_pct else "OK"
        days_until = (policy.expiration_date - today).days

        report.append(
            RenewalReportRow(
                policy_id=policy.id,
                customer_id=customer.id,
                customer_name=customer.full_name,
                policy_number=policy.policy_number,
                carrier=policy.carrier,
                product_type=policy.product_type,
                effective_date=policy.effective_date,
                expiration_date=policy.expiration_date,
                days_until_expiration=days_until,
                old_premium=old_p,
                renewal_premium=new_p,
                pct_change=round(pct, 2),
                flag=flag,
            )
        )

    return report
