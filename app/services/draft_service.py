from sqlalchemy.orm import Session, joinedload

from app.models.policy import Policy
from app.models.message_template import MessageTemplate
from app.services.template_renderer import render_template
from app.services.renewal_service import _calc_increase


def build_renewal_draft_text(
    db: Session,
    *,
    policy_id: int,
    template_name: str,
) -> tuple[str, str]:
    """
    Returns (channel, draft_text)
    """
    policy = (
        db.query(Policy)
        .options(joinedload(Policy.customer))
        .filter(Policy.id == policy_id)
        .first()
    )
    if not policy:
        raise ValueError("Policy not found")

    template = (
        db.query(MessageTemplate).filter(MessageTemplate.name == template_name).first()
    )
    if not template:
        raise ValueError("Template not found")

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
    return template.channel, draft_text
