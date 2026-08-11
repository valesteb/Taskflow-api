from fastapi import FastAPI
from app.models.project import Project
from app.services import project_service

app = FastAPI(
    title="TaskFlow API",
    description="Backend API for project management",
    version="0.1.0"
)

@app.get("/")
def root():
    return {
        "message": "Welcome to the TaskFlow API!"
    }

@app.get("/projects")
def get_projects():
    return project_service.get_projects()

@app.get("/projects/{project_id}")
def get_project_by_id(project_id: int):
    return project_service.get_project_by_id(project_id)



@app.post("/projects", status_code=201)
def create_project(project: Project):
    return project_service.create_project(project)

@app.delete("/projects/{project_id}, status_code=204")
def delete_project(project_id: int):
    return project_service.delete_project(project_id)