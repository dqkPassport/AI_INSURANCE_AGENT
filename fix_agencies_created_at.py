from sqlalchemy import text
from app.db.session import engine

with engine.begin() as conn:
    conn.execute(
        text(
            "UPDATE agencies SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL"
        )
    )
    print("Backfilled agencies.created_at where it was NULL.")
