from fastapi import APIRouter, HTTPException
from typing import List
from app.models.projects import Project, ProjectCreate, ProjectBase, get_project_by_id, get_all_projects, create_project, update_project, delete_project

router = APIRouter()

@router.post("/projects/", response_model=Project, tags=["Projects"])
async def create_project_endpoint(project: ProjectCreate):
    """ 
    Create a new project. 
    """
    created_project = await create_project(project)
    return created_project

@router.get("/projects/", response_model=List[Project], tags=["Projects"])
async def get_projects_endpoint():
    """ 
    Retrieve all projects. 
    """
    projects = await get_all_projects()
    return projects

@router.get("/projects/{project_id}", response_model=Project, tags=["Projects"])
async def get_project_endpoint(project_id: str):
    """ 
    Retrieve a project by its ID.
    """
    project = await get_project_by_id(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/projects/{project_id}", response_model=Project, tags=["Projects"])
async def update_project_endpoint(project_id: str, project_data: ProjectBase):
    """ 
    Update an existing project by its ID.
    """
    updated_project = await update_project(project_id, project_data)
    if updated_project is None:
        raise HTTPException(status_code=404, detail="Project not found or could not be updated")
    return updated_project

@router.delete("/projects/{project_id}", response_model=dict, tags=["Projects"])
async def delete_project_endpoint(project_id: str):
    """ 
    Delete a project by its ID.
    """
    deleted = await delete_project(project_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Project not found or could not be deleted")
    return {"message": "Project successfully deleted"}
