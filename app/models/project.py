from pydantic import BaseModel

class Project(BaseModel):
    id: int
    name: str
    status: str

class ProjectUpdate(BaseModel):
    name: str | None = None
    status: str | None = None

    