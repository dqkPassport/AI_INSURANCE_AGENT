from fastapi import FastAPI

from app.db.session import engine
from app.db.base import Base
import app.models  # important: loads models
from app.api.router import api_router

app = FastAPI(title="AI Insurance Agent", version="0.1.0")

# Because now we use Alembic, so we don't need it anymore
# @app.on_event("startup")
# def on_startup():
#     Base.metadata.create_all(bind=engine)


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(api_router)
