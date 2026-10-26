from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.models import Project as ProjectDB
from app.db.database import SessionLocal


with SessionLocal() as session:
    statement = select(ProjectDB)
    projects = session.scalars(statement).all()

    for project in projects:
        print(project.id, project.name, project.status)

