import csv
import io
from typing import Iterable

from app.services.renewals_report import RenewalReportRow


def renewals_to_csv(rows: Iterable[RenewalReportRow]) -> str:
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(
        [
            "policy_id",
            "customer_id",
            "customer_name",
            "policy_number",
            "carrier",
            "product_type",
            "effective_date",
            "expiration_date",
            "days_until_expiration",
            "old_premium",
            "renewal_premium",
            "pct_change",
            "flag",
        ]
    )

    for r in rows:
        writer.writerow(
            [
                r.policy_id,
                r.customer_id,
                r.customer_name,
                r.policy_number,
                r.carrier,
                r.product_type,
                r.effective_date.isoformat(),
                r.expiration_date.isoformat(),
                r.days_until_expiration,
                r.old_premium,
                r.renewal_premium,
                r.pct_change,
                r.flag,
            ]
        )

    return output.getvalue()
