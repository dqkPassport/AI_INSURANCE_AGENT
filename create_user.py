from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import hash_password

db = SessionLocal()

email = "admin@demo.com"
password = "admin123"
agency_id = 1
print("pw len:", len(password.encode("utf-8")))

user = User(
    email=email,
    hashed_password=hash_password(password),
    agency_id=agency_id,
    role="admin",
)
db.add(user)
db.commit()
print("Created user:", email, "pw:", password)

db.close()
