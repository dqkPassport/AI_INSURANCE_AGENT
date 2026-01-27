from fastapi import APIRouter
from app.api.routes.customers import router as customers_router
from app.api.routes.policies import router as policies_router
from app.api.routes.renewals import router as renewals_router
from app.api.routes.interactions import router as interactions_router
from app.api.routes.tasks import router as tasks_router
from app.api.routes.renewal_plan import router as renewal_plan_router
from app.api.routes.customer_overview import router as customer_overview_router
from app.api.routes.templates import router as templates_router
from app.api.routes.drafts import router as drafts_router
from app.api.routes.ai import router as ai_router
from app.api.routes.ai_logs import router as ai_logs_router
from app.api.routes.agencies import router as agencies_router
from app.api.routes.auth import router as auth_router

api_router = APIRouter()
api_router.include_router(customers_router)
api_router.include_router(policies_router)
api_router.include_router(renewals_router)
api_router.include_router(interactions_router)
api_router.include_router(tasks_router)
api_router.include_router(renewal_plan_router)
api_router.include_router(customer_overview_router)
api_router.include_router(templates_router)
api_router.include_router(drafts_router)
api_router.include_router(ai_router)
api_router.include_router(ai_logs_router)
api_router.include_router(agencies_router)
api_router.include_router(auth_router)
