from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_project_by_id():
    response = client.get("/projects/1")
    assert response.status_code == 200