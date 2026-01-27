from sqlalchemy import text
from app.db.session import engine

with engine.begin() as conn:
    conn.execute(text("DROP TABLE IF EXISTS _alembic_tmp_agencies"))
    print("Dropped _alembic_tmp_agencies (if it existed).")
