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
    
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "int_parsing"
    assert response.json()["detail"][0]["loc"] == ["body", "id"]

def test_create_project_invalid_name():
    response = client.post(
        "/projects",
        json={
            "id": 4,
            "name": 123,
            "status": "In progress"
        }
    )
    
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "string_type"
    assert response.json()["detail"][0]["loc"] == ["body", "name"]

def test_create_project_invalid_status():
    response = client.post(
        "/projects",
        json={
            "id": 5,
            "name": "Invalid Status Project",
            "status": 123
        }
    )
    
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "string_type"
    assert response.json()["detail"][0]["loc"] == ["body", "status"]

def test_update_project_invalid_name():
    response = client.patch(
        "/projects/1",
        json={
            "name": 123
        }
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "string_type"
    assert response.json()["detail"][0]["loc"] == ["body", "name"]

def test_update_project_invalid_status():
    response = client.patch(
        "/projects/1",
        json={
            "status": 123
        }
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "string_type"
    assert response.json()["detail"][0]["loc"] == ["body", "status"]

def test_update_project_without_fields():
    response = client.patch(
        "/projects/1",
        json={}
    )
    assert response.status_code == 422
    assert response.json()["detail"] == "At least one field must be provided for update"

def test_update_project_name_only():
    response = client.patch(
        "/projects/1",
        json={
            "name": "Updated TaskFlow API"
        }
    )
    
    assert response.status_code == 200
    assert response.json()["name"] == "Updated TaskFlow API"
    assert response.json()["status"] == "In Progress"

def test_update_project_status_only():
    response = client.patch(
        "/projects/1",
        json={
            "status": "Completed"
        }
    )
    assert response.status_code == 200
    assert response.json()["name"] == "TaskFlow API"
    assert response.json()["status"] == "Completed"

def test_replace_project():
    response = client.put(
        "/projects/1",
        json={
            "id": 1,
            "name": "Replaced TaskFlow API",
            "status": "Completed"
        }
    )

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == "Replaced TaskFlow API"
    assert response.json()["status"] == "Completed"

    get_response = client.get("/projects/1")

    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Replaced TaskFlow API"
    assert get_response.json()["status"] == "Completed"