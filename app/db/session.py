from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.settings import settings

DATABASE_URL = settings.database_url

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # needed for SQLite + FastAPI
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
