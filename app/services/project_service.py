from app.models.project import Project, ProjectUpdate
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

def update_project(project_id: int, project_update: ProjectUpdate):
    existing_project = project_repository.get_project_by_id(project_id)

    if existing_project is None:
        raise HTTPException(
            status_code=404,
            detail=f"Project with ID {project_id} not found"
        )

    if project_update.name is None and project_update.status is None:
        raise HTTPException(
            status_code=422,
            detail="At least one field must be provided for update"
        )

    return project_repository.update_project(
        existing_project,
        project_update
    )

def replace_project(project_id: int, new_project: Project):
    existing_project = project_repository.get_project_by_id(project_id)

    if existing_project is None:
        raise HTTPException(
            status_code=404,
            detail=f"Project with ID {project_id} not found"
        )
    if project_id != new_project.id:
        raise HTTPException(
            status_code = 409,
            detail = "Project ID in URL and request body do not match"
        )
    return project_repository.replace_project(
        existing_project,
        new_project
        )
