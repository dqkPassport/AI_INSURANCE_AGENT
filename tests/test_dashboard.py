from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_dashboard():
    r = client.get("/dashboard/summary")
    assert r.status_code in (401, 403)
