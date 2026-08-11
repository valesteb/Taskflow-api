from app.models.project import Project
from app.repositories import project_repository
from fastapi import HTTPException

def get_projects():
    return project_repository.get_all_projects()

def get_project_by_id(project_id: int):
    existing_project = project_repository.get_project_by_id(project_id)

    if existing_project is None:
        raise HTTPException(
            status_code=404,
            detail=f"Project with ID {project_id} not found!"
        )
    return existing_project

def create_project(project: Project):
    existing_project = project_repository.get_project_by_id(project.id)

    if existing_project is None:
        return project_repository.add_project(project)
    
    raise HTTPException(
        status_code=409,
        detail=f"project with ID {project.id} already exists! "
    )

def delete_project_by_id(project_id: int):
    existing_project = project_repository.get_project_by_id(project_id)

    if existing_project is None:
        raise HTTPException(
            status_code=404,
            detail=f"Project with ID {project_id} not found"
        )

    return project_repository.delete_project(existing_project)  

