from pydantic import BaseModel
from typing import Optional, List

# In-memory storage for demonstration purposes
projects_db = {}

class ProjectBase(BaseModel):
    name: str

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: str

    class Config:
        orm_mode = True

async def create_project(project: ProjectCreate) -> Project:
    project_id = "nhdyrsWGRkkutte343"  # Static project ID for demonstration
    new_project = Project(id=project_id, **project.dict())
    projects_db[project_id] = new_project
    return new_project



async def get_project_by_id(project_id: str) -> Optional[Project]:
    return projects_db.get(project_id)

async def get_all_projects() -> List[Project]:
    return list(projects_db.values())

async def update_project(project_id: str, project_data: ProjectBase) -> Optional[Project]:
    if project_id in projects_db:
        existing_project = projects_db[project_id]
        updated_project = existing_project.copy(update=project_data.dict())
        projects_db[project_id] = updated_project
        return updated_project
    return None

async def delete_project(project_id: str) -> bool:
    if project_id in projects_db:
        del projects_db[project_id]
        return True
    return False
