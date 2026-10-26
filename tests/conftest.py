import os
import pytest

from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, delete
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker

from app.db.database import get_db
from app.db.models import Base, Project as ProjectDB
from app.main import app


load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if not TEST_DATABASE_URL:
    raise ValueError("TEST_DATABASE_URL is not configured.")

if make_url(TEST_DATABASE_URL).database != "taskflow_test":
    raise ValueError("TEST_DATABASE_URL must be in the 'taskflow_test' database.")


test_engine = create_engine(TEST_DATABASE_URL)


TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autocommit=False,
    autoflush=False)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def reset_test_database():
    Base.metadata.create_all(bind=test_engine)

    db = TestingSessionLocal()

    try:
        db.execute(delete(ProjectDB))

        db.add_all([
            ProjectDB(
                id=1,
                name="TaskFlow API",
                status="In Progress"
            ),
            ProjectDB(
                id=2,
                name="Personal Portfolio",
                status="Completed"
            )
        ])

        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

    yield