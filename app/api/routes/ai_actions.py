from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.auth_deps import get_current_agency_id
from app.models.policy import Policy
from app.schemas.ai_actions import GenerateTasksOut, GenerateTasksRequest
from app.services.actions_service import generate_tasks_for_policy

router = APIRouter(prefix="/ai/actions", tags=["ai"])


@router.post("/policy/{policy_id}/generate-tasks", response_model=GenerateTasksOut)
def generate_tasks(
    policy_id: int,
    payload: GenerateTasksRequest,
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

    tasks = generate_tasks_for_policy(
        db=db,
        agency_id=agency_id,
        policy=policy,
        req=payload,
    )

    return GenerateTasksOut(policy_id=policy_id, created_count=len(tasks), tasks=tasks)
