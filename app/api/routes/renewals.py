from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.config import DEFAULT_RENEWAL_DAYS, DEFAULT_SHOCK_THRESHOLD
from app.schemas.renewal import RenewalOut
from app.services.renewal_service import get_renewals
from app.core.tenant import get_agency_id

from app.core.auth_deps import get_current_agency_id
from app.services.renewals_report import build_renewals_report
from app.utils.csv_export import renewals_to_csv

router = APIRouter(prefix="/renewals", tags=["renewals"])


@router.get("", response_model=list[RenewalOut])
def list_renewals(
    days: int = Query(DEFAULT_RENEWAL_DAYS, ge=1, le=365),
    shock_threshold: float = Query(DEFAULT_SHOCK_THRESHOLD, ge=0, le=1),
    db: Session = Depends(get_db),
    agency_id: int = Depends(get_agency_id),
):
    items = get_renewals(db, days=days, shock_threshold=shock_threshold)

    # Convert RenewalItem -> RenewalOut
    out: list[RenewalOut] = []
    for item in items:
        p = item.policy
        out.append(
            RenewalOut(
                policy_id=p.id,
                customer_id=p.customer_id,
                customer_name=p.customer.full_name if p.customer else "Unknown",
                policy_number=p.policy_number,
                carrier=p.carrier,
                product_type=p.product_type,
                effective_date=p.effective_date,
                expiration_date=p.expiration_date,
                old_premium=p.old_premium,
                renewal_premium=p.renewal_premium,
                days_to_expire=item.days_to_expire,
                increase_amount=item.increase_amount,
                increase_pct=item.increase_pct,
                is_shock=item.is_shock,
            )
        )

    return out


@router.get("/export")
def export_renewals_csv(
    days: int = Query(30, ge=1, le=365),
    shock_threshold_pct: float = Query(10.0, ge=0, le=500),
    db: Session = Depends(get_db),
    agency_id: int = Depends(get_current_agency_id),
):
    report_rows = build_renewals_report(
        db=db,
        agency_id=agency_id,
        days=days,
        shock_threshold_pct=shock_threshold_pct,
    )
    csv_text = renewals_to_csv(report_rows)

    filename = f"renewals_next_{days}_days.csv"
    return Response(
        content=csv_text,
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
