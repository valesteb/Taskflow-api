from app.models.project import Project

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

def get_all_projects():
    return projects

def add_project(project: Project):
    projects.append(project)
    return project

def get_project_by_id(project_id: int):
    for project in projects:
        if project.id == project_id:
            return project
    return None

def delete_project(project: Project):
    projects.remove(project)
    return project

