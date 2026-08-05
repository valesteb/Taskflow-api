from app.models.project import Project
from app.repositories import project_repository

def get_projects():
    return project_repository.get_all_projects()

def create_project(project: Project):
    existing_project = project_repository.get_project_by_id(project.id)

    if existing_project is None:
        return project_repository.add_project(project)
    return existing_project