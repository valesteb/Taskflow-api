from copy import deepcopy
from fastapi.testclient import TestClient
from app.main import app
from app.repositories.project_repository import projects
import pytest

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_projects():
    original_projects = deepcopy(projects)

    yield

    projects.clear()
    projects.extend(original_projects)

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
    assert response.status_code == 201
    assert response.json()["id"] == 3
    assert response.json()["name"] == "New Project"
    assert response.json()["status"] == "In Progress"

def test_delete_project():
    delete_response = client.delete("/projects/2")

    assert delete_response.status_code == 204

    get_response = client.get("/projects/2")
    assert get_response.status_code == 404

def test_delete_nonexistent_project():
    response = client.delete("/projects/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Project with ID 999 not found"
    
def test_project_two_exists():
    response = client.get("/projects/2")
    assert response.status_code == 200
    
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

def test_update_nonexistent_project():
    response = client.patch(
        "/projects/999",
        json={
            "name": "Updated Project Name",
            "status": "Completed"
        }
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Project with ID 999 not found"
    
def test_create_duplicate_project():
    response = client.post(
        "/projects",
        json={
            "id": 1,
            "name": "Duplicate Project",
            "status": "In progress"
        }
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "project with ID 1 already exists! "

def test_create_project_invalid_id():
    response = client.post(
        "/projects",
        json={
            "id": "hola",
            "name": "Invalid ID project",
            "status": "In progress"
        }
    )
    print(response.json())
    assert response.status_code == 422

    