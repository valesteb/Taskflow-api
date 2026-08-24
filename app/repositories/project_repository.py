from app.models.project import Project, ProjectUpdate


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

def update_project(project: Project, project_update: ProjectUpdate):
    if project_update.name:
        project.name = project_update.name
    if project_update.status:
        project.status = project_update.status

    return project

def replace_project(existing_project: Project, new_project: Project):
    for index, project in enumerate(projects):
        if project.id == existing_project.id:
            project[index] = new_project
            return new_project
        

