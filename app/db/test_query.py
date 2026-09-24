from sqlalchemy import select
from app.db.models import Project
from app.db.database import SessionLocal

with SessionLocal() as session:
    statement = select(Project)
    projects = session.scalars(statement).all()

    for project in projects:
        print(project.id, project.name, project.status)

