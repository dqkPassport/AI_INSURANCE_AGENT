from datetime import date
from pydantic import BaseModel


class DashboardSummaryOut(BaseModel):
    customers_total: int
    policies_total: int
    policies_expiring_30_days: int
    open_tasks_total: int
    tasks_due_next_7_days: int
    interactions_last_7_days: int
    today: date
