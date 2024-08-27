from fastapi import Depends, HTTPException, APIRouter
from typing import List
from app.models.milestones import Milestones, MilestonesBase, MilestonesCreate, create_milestones, get_milestoness, get_milestones_by_id, delete_milestones, update_milestones, get_milestoness_by_project_id
from app.routes.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/milestones/", response_model=Milestones, tags=["Milestones"])
async def create_milestones_endpoint(milestones: MilestonesCreate, current_user: User = Depends(get_current_user)):
    """ 
    Create a new milestone.
    
    Args:
        milestones (MilestonesCreate): Data for the new milestone.
        current_user (User): Current logged-in user.
        
    Returns:
        Milestones: Details of the created milestone.
    """
    milestones_data = await create_milestones(milestones)
    return milestones_data

@router.get("/milestones/", response_model=List[Milestones], tags=["Milestones"])
async def get_milestoness(skip: int = 0, limit: int = 10):
    """ 
    Retrieve a list of milestones with pagination.
    
    Args:
        skip (int): Number of milestones to skip. Defaults to 0.
        limit (int): Maximum number of milestones to return. Defaults to 10.
        
    Returns:
        List[Milestones]: List of milestones within the specified range.
    """
    milestoness = await get_milestoness(skip=skip, limit=limit)
    return milestoness

@router.get("/milestones/{id}", response_model=Milestones, tags=["Milestones"])
async def get_milestones(id: str):
    """ 
    Retrieve a single milestone by its ID.
    
    Args:
        id (str): ID of the milestone to retrieve.
        
    Returns:
        Milestones: The milestone with the specified ID.
        
    Raises:
        HTTPException: If no milestone is found with the provided ID.
    """
    milestone = await get_milestones_by_id(id)
    if milestone is None:
        raise HTTPException(status_code=404, detail="Milestone with the given ID does not exist. Please check the ID and try again.")
    return milestone

@router.put("/milestones/{id}", response_model=Milestones, tags=["Milestones"])
async def update_milestones_endpoint(id: str, milestones_data: MilestonesBase, current_user: User = Depends(get_current_user)):
    """ 
    Update an existing milestone by its ID.
    
    Args:
        id (str): ID of the milestone to update.
        milestones_data (MilestonesBase): Updated milestone data.
        
    Returns:
        Milestones: The updated milestone.
        
    Raises:
        HTTPException: If no milestone is found with the specified ID.
    """
    updated_milestone = await update_milestones(id, milestones_data)
    if updated_milestone is None:
        raise HTTPException(status_code=404, detail="Milestone with the given ID does not exist or could not be updated. Please check the ID and try again.")
    return updated_milestone

@router.get("/projects/{project_id}/milestones/", response_model=List[Milestones], tags=["Milestones"])
async def get_milestoness_by_project(project_id: str, skip: int = 0, limit: int = 10):
    """ 
    Retrieve milestones associated with a specific project ID with pagination.
    
    Args:
        project_id (str): ID of the project whose milestones are to be retrieved.
        skip (int): Number of milestones to skip. Defaults to 0.
        limit (int): Maximum number of milestones to return. Defaults to 10.
        
    Returns:
        List[Milestones]: List of milestones related to the specified project.
        
    Raises:
        HTTPException: If no milestones are found for the provided project ID.
    """
    milestoness = await get_milestoness_by_project_id(project_id, skip=skip, limit=limit)
    if not milestoness:
        raise HTTPException(status_code=404, detail="No milestones found for the project with the given ID. Please verify the project ID.")
    return milestoness

@router.delete("/milestones/{id}", response_model=dict, tags=["Milestones"])
async def delete_milestones_endpoint(id: str, current_user: User = Depends(get_current_user)):
    """ 
    Delete a milestone by its ID.
    
    Args:
        id (str): ID of the milestone to delete.
        
    Returns:
        dict: Message indicating the result of the delete operation.
        
    Raises:
        HTTPException: If no milestone is found with the specified ID.
    """
    deleted = await delete_milestones(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Milestone with the given ID does not exist or could not be deleted. Please check the ID and try again.")
    return {"message": "Milestone successfully deleted."}
