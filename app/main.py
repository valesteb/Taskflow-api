from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.models import Project as ProjectDB
from app.db.database import get_db
from app.models.project import Project, ProjectUpdate
from app.services import project_service

app = FastAPI(
    title="TaskFlow API",
    description="Backend API for project management",
    version="0.1.0"
)

@app.get("/db-test")
def db_test(db: Session = Depends(get_db)):
    statement = select(ProjectDB)
    projects = db.scalars(statement).all()

    return projects

@app.get("/")
def root():
    return {
        "message": "Welcome to the TaskFlow API!"
    }

@app.get("/projects")
def get_projects(db: Session = Depends(get_db)):
    return project_service.get_projects(db)

@app.get("/projects/{project_id}")
def get_project_by_id(
    project_id: int,
    db: Session = Depends(get_db)
):
    return project_service.get_project_by_id(project_id, db)

@app.post("/projects", status_code=201)
def create_project(
    project: Project,
    db: Session = Depends(get_db)
):
    return project_service.create_project(project, db)

@app.delete("/projects/{project_id}", status_code=204)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    return project_service.delete_project_by_id(project_id, db)

@app.patch("/projects/{project_id}", status_code=200)
def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    db: Session = Depends(get_db)
):
    return project_service.update_project(project_id, project_update, db)

@app.put("/projects/{project_id}")
def replace_project(
    project_id:int,
    new_project: Project,
    db: Session = Depends(get_db)
):
    return project_service.replace_project(project_id, new_project, db)