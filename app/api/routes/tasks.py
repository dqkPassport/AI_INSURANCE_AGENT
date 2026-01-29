from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskOut
from app.core.auth_deps import get_current_agency_id

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskOut)
def create_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
    agency_id: int = Depends(get_current_agency_id),
):
    task = Task(agency_id=agency_id, **payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("", response_model=list[TaskOut])
def list_tasks(
    status: str | None = Query(None),  # open/done
    customer_id: int | None = Query(None),
    policy_id: int | None = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(Task).order_by(Task.due_date.asc(), Task.id.desc())

    if status is not None:
        q = q.filter(Task.status == status)
    if customer_id is not None:
        q = q.filter(Task.customer_id == customer_id)
    if policy_id is not None:
        q = q.filter(Task.policy_id == policy_id)

    return q.all()


@router.patch("/{task_id}/done", response_model=TaskOut)
def mark_task_done(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = "done"
    db.commit()
    db.refresh(task)
    return task
