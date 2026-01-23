from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.api.deps import get_db
from app.models.policy import Policy
from app.models.message_template import MessageTemplate
from app.schemas.draft import DraftRenewalRequest, DraftRenewalTonesRequest, DraftOut
from app.services.template_renderer import render_template
from app.services.renewal_service import _calc_increase

router = APIRouter(prefix="/drafts", tags=["drafts"])


@router.post("/renewal-message", response_model=DraftOut)
def draft_renewal_message(payload: DraftRenewalRequest, db: Session = Depends(get_db)):
    policy = (
        db.query(Policy)
        .options(joinedload(Policy.customer))
        .filter(Policy.id == payload.policy_id)
        .first()
    )
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")

    template = (
        db.query(MessageTemplate)
        .filter(MessageTemplate.name == payload.template_name)
        .first()
    )
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    inc_amount, inc_pct = _calc_increase(policy.old_premium, policy.renewal_premium)

    context = {
        "customer_name": policy.customer.full_name if policy.customer else "Customer",
        "policy_number": policy.policy_number,
        "carrier": policy.carrier,
        "product_type": policy.product_type,
        "effective_date": policy.effective_date,
        "expiration_date": policy.expiration_date,
        "old_premium": policy.old_premium,
        "renewal_premium": policy.renewal_premium,
        "increase_amount": inc_amount,
        "increase_pct": (round(inc_pct * 100, 1) if inc_pct is not None else None),
    }

    draft_text = render_template(template.body, context)

    return DraftOut(
        template_name=template.name,
        channel=template.channel,
        draft_text=draft_text,
    )


@router.post("/renewal-message/tones", response_model=list[DraftOut])
def draft_renewal_message_tones(
    payload: DraftRenewalTonesRequest, db: Session = Depends(get_db)
):
    # 1) Load policy + customer once
    policy = (
        db.query(Policy)
        .options(joinedload(Policy.customer))
        .filter(Policy.id == payload.policy_id)
        .first()
    )
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")

    # 2) Load all templates in one query
    templates = (
        db.query(MessageTemplate)
        .filter(MessageTemplate.name.in_(payload.template_names))
        .all()
    )

    found = {t.name: t for t in templates}
    missing = [name for name in payload.template_names if name not in found]
    if missing:
        raise HTTPException(status_code=404, detail=f"Missing templates: {missing}")

    # 3) Build context once
    inc_amount, inc_pct = _calc_increase(policy.old_premium, policy.renewal_premium)
    context = {
        "customer_name": policy.customer.full_name if policy.customer else "Customer",
        "policy_number": policy.policy_number,
        "carrier": policy.carrier,
        "product_type": policy.product_type,
        "effective_date": policy.effective_date,
        "expiration_date": policy.expiration_date,
        "old_premium": policy.old_premium,
        "renewal_premium": policy.renewal_premium,
        "increase_amount": inc_amount,
        "increase_pct": (round(inc_pct * 100, 1) if inc_pct is not None else None),
    }

    # 4) Render drafts in the SAME ORDER as the request
    out: list[DraftOut] = []
    for name in payload.template_names:
        t = found[name]
        out.append(
            DraftOut(
                template_name=t.name,
                channel=t.channel,
                draft_text=render_template(t.body, context),
            )
        )

    return out
