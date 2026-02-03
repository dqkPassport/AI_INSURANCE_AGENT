from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.auth_deps import get_current_agency_id
from app.models.policy import Policy
from app.schemas.ai_suggestions import SuggestionsResponse
from app.services.suggestions_service import build_policy_suggestions

router = APIRouter(prefix="/ai/suggestions", tags=["ai"])


@router.get("/policy", response_model=SuggestionsResponse)
def get_policy_suggestions(
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

    suggestions = build_policy_suggestions(
        expiration_date=policy.expiration_date,
        old_premium=float(policy.old_premium or 0),
        renewal_premium=float(policy.renewal_premium or 0),
    )

    return SuggestionsResponse(policy_id=policy_id, suggestions=suggestions)
