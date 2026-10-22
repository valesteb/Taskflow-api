from app.models.project import Project, ProjectUpdate
from app.db.models import Project as ProjectDB

from sqlalchemy.orm import Session
from sqlalchemy import select




projects = [
    Project(
        id=1,
        name="TaskFlow API",
        status="In Progress"
    ),
    Project(
        id=2,
        name="Personal Portfolio",
        status="Completed"
    )
]

def get_all_projects(db: Session):
    statement = select(ProjectDB)
    return db.scalars(statement).all()

def add_project(project: Project, db: Session):
    project_db = ProjectDB(
        id=project.id,
        name=project.name,
        status=project.status
    )

    db.add(project_db)
    db.commit()
    db.refresh(project_db)

    return project_db

def get_project_by_id(project_id: int, db: Session):
    statement = select(ProjectDB).where(ProjectDB.id == project_id)
    return db.scalars(statement).first()


def delete_project(project: ProjectDB, db: Session):
    db.delete(project)
    db.commit()
    return project

def update_project(project: Project, project_update: ProjectUpdate):
    if project_update.name:
        project.name = project_update.name
    if project_update.status:
        project.status = project_update.status

    return project

def replace_project(existing_project: Project, new_project: Project):
    for index, project in enumerate(projects):
        if project.id == existing_project.id:
            projects[index] = new_project
            return new_project
        

