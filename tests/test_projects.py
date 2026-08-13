from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_project_by_id():
    response = client.get("/projects/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_nonexistent_project():
    response = client.get("/projects/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Project with ID 999 not found!"

def test_create_project():
    response = client.post(
        "/projects",
        json={
        "id": 3,
        "name": "New Project",
        "status": "In Progress"
        }
    )

def test_delete_project():
    delete_response = client.delete("/projects/2")

    assert delete_response.status_code == 204

    get_response = client.get("/projects/2")
    assert get_response.status_code == 404

def test_update_project():
    response = client.patch(
        "/projects/1",
        json={
            "name": "Updated Project Name",
            "status": "Completed"
        }
    )
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == "Updated Project Name"
    assert response.json()["status"] == "Completed"
    
