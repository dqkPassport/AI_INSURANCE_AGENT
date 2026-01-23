from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.ai_log import AiRewriteLog
from app.schemas.ai_log import AiLogOut

router = APIRouter(prefix="/ai-logs", tags=["ai-logs"])


@router.get("", response_model=list[AiLogOut])
def list_ai_logs(
    policy_id: int | None = Query(None),
    limit: int = Query(50, ge=11, le=200),
    db: Session = Depends(get_db),
):
    q = db.query(AiRewriteLog).order_by(AiRewriteLog.id.desc())
    if policy_id is not None:
        q = q.filter(AiRewriteLog.policy_id == policy_id)
    return q.limit(limit).all()
