from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services import project_service

router = APIRouter()

@router.get("/projects")
def get_projects(db: Session = Depends(get_db)):
    return project_service.get_projects(db)

@router.get("/projects/{project_id}")
def get_project_by_id(
    project_id: int,
    db: Session = Depends(get_db)
):
    return project_service.get_project_by_id(project_id, db)

@router.post("/projects", status_code=201)
def create_project(
    project: Project,
    db: Session = Depends(get_db)
):
    return project_service.create_project(project, db)
