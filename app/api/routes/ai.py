from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.ai import (
    RewriteRequest,
    RewriteOut,
    RewriteFromPolicyRequest,
    RewriteFromPolicyOut,
)
from app.services.ai_service import rewrite_message
from app.services.draft_service import build_renewal_draft_text
from app.models.ai_log import AiRewriteLog
from app.services.rewrite_validator import validate_no_fact_change

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/rewrite", response_model=RewriteOut)
def rewrite(payload: RewriteRequest):
    rewritten = rewrite_message(
        text=payload.text, tone=payload.tone, channel=payload.channel
    )
    return RewriteOut(
        tone=payload.tone, channel=payload.channel, rewritten_text=rewritten
    )


@router.post("/rewrite-from-policy", response_model=RewriteFromPolicyOut)
def rewrite_from_policy(
    payload: RewriteFromPolicyRequest,
    strict: bool = True,
    db: Session = Depends(get_db),
):
    try:
        template_channel, base_draft = build_renewal_draft_text(
            db,
            policy_id=payload.policy_id,
            template_name=payload.template_name,
        )
    except ValueError as e:
        msg = str(e)
        if "Policy" in msg:
            raise HTTPException(status_code=404, detail=msg)
        if "Template" in msg:
            raise HTTPException(status_code=404, detail=msg)
        raise HTTPException(status_code=400, detail=msg)

    # Use payload.channel if provided; otherwise use template channel
    channel = payload.channel or template_channel

    rewritten = rewrite_message(text=base_draft, tone=payload.tone, channel=channel)

    ok, err = validate_no_fact_change(base_draft, rewritten)
    log = AiRewriteLog(
        policy_id=payload.policy_id,
        template_name=payload.template_name,
        tone=payload.tone,
        channel=channel,
        base_text=base_draft,
        rewritten_text=rewritten,
        validation_passed=ok,
        validation_error=err,
    )
    db.add(log)
    db.commit()
    db.refresh
    if not ok and strict:
        raise HTTPException(
            status_code=400,
            detail=f"Rewrite blocked by validation. {err}",
        )
    warning = None
    if not ok and not strict:
        warning = f"Validation failed :{err}"

    return RewriteFromPolicyOut(
        policy_id=payload.policy_id,
        template_name=payload.template_name,
        tone=payload.tone,
        channel=channel,
        base_draft=base_draft,
        rewritten_draft=rewritten,
        warning=warning,
    )
