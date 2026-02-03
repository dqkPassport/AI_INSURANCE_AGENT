from __future__ import annotations

from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.models.policy import Policy
from app.models.task import Task
from app.schemas.ai_actions import GenerateTasksRequest, GeneratedTaskOut
from app.services.suggestions_service import build_policy_suggestions


def _task_priority_from_suggestion_priority(p: int) -> str:
    if p <= 2:
        return "high"
    if p == 3:
        return "normal"
    return "low"


def _task_title_from_suggestion(suggestion_type: str, title: str) -> str:
    prefix = {
        "call": "Call",
        "sms": "Text",
        "email": "Email",
        "task": "Task",
        "note": "Note",
    }.get(suggestion_type, "Action")
    return f"{prefix}: {title}"


def generate_tasks_for_policy(
    *,
    db: Session,
    agency_id: int,
    policy: Policy,
    req: GenerateTasksRequest,
) -> list[GeneratedTaskOut]:
    # Build suggestions from policy facts (Day 16 rules)
    suggestions = build_policy_suggestions(
        expiration_date=policy.expiration_date,
        old_premium=float(policy.old_premium or 0),
        renewal_premium=float(policy.renewal_premium or 0),
    )

    wanted = set(req.include_types)
    due_date = date.today() + timedelta(days=req.due_in_days)

    created: list[GeneratedTaskOut] = []

    for s in suggestions:
        if s.type not in wanted:
            continue

        title = _task_title_from_suggestion(s.type, s.title)

        # Basic duplicate prevention: if an open task with same title already exists, skip it.
        exists = (
            db.query(Task.id)
            .filter(Task.agency_id == agency_id)
            .filter(Task.policy_id == policy.id)
            .filter(Task.status == "open")
            .filter(Task.title == title)
            .first()
        )
        if exists:
            continue

        task_obj = Task(
            agency_id=agency_id,
            customer_id=policy.customer_id,
            policy_id=policy.id,
            title=title,
            status="open",
            priority=_task_priority_from_suggestion_priority(s.priority),
            due_date=due_date,
        )

        if not req.dry_run:
            db.add(task_obj)

        created.append(
            GeneratedTaskOut(
                title=task_obj.title,
                status=task_obj.status,
                priority=task_obj.priority,
                customer_id=task_obj.customer_id,
                policy_id=task_obj.policy_id,
            )
        )

    if not req.dry_run and created:
        db.commit()

    return created
