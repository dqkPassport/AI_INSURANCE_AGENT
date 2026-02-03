from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.auth_deps import get_current_agency_id
from app.models.customer import Customer
from app.models.policy import Policy
from app.schemas.ai_draft import (
    DraftRenewalFromPolicyRequest,
    DraftRenewalOut,
    DraftRenewalRequest,
    RenewalFacts,
)
from app.services.ai_draft_service import draft_renewal_message

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/draft-renewal", response_model=DraftRenewalOut)
def draft_renewal(payload: DraftRenewalRequest):
    try:
        text = draft_renewal_message(
            facts=payload.facts,
            tone=payload.tone,
            channel=payload.channel,
            strict=True,  # always strict when user provides facts
        )
        return DraftRenewalOut(
            tone=payload.tone, channel=payload.channel, drafted_text=text
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/draft-renewal-from-policy", response_model=DraftRenewalOut)
def draft_renewal_from_policy(
    payload: DraftRenewalFromPolicyRequest,
    policy_id: int = Query(..., ge=1),
    db: Session = Depends(get_db),
    agency_id: int = Depends(get_current_agency_id),
):
    policy = (
        db.query(Policy)
        .filter(Policy.id == policy_id)
        .filter(Policy.agency_id == agency_id)
        .first()
    )
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")

    customer = (
        db.query(Customer)
        .filter(Customer.id == policy.customer_id)
        .filter(Customer.agency_id == agency_id)
        .first()
    )
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    facts = RenewalFacts(
        customer_name=customer.full_name,
        policy_number=policy.policy_number,
        carrier=policy.carrier,
        product_type=policy.product_type,
        expiration_date=policy.expiration_date,
        old_premium=float(policy.old_premium or 0),
        renewal_premium=float(policy.renewal_premium or 0),
    )

    try:
        text = draft_renewal_message(
            facts=facts,
            tone=payload.tone,
            channel=payload.channel,
            strict=payload.strict,
        )
        return DraftRenewalOut(
            tone=payload.tone, channel=payload.channel, drafted_text=text
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
