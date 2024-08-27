from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.progress import Progress, ProgressCreate, create_progress, get_progress_by_user_id, update_progress, delete_progress
from app.models.user import get_user_by_username

router = APIRouter()

@router.post("/progress/", response_model=Progress, tags=["Progress"])
async def register_progress(progress: ProgressCreate):
    """ 
    Create a new progress entry. 
    """
    # Verify if the user associated with the progress exists
    user = await get_user_by_username(progress.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User with the specified ID not found. Please verify the user ID.")
    
    # Create and return the new progress entry
    progress_data = await create_progress(progress)
    return progress_data

@router.get("/progress/user/{user_id}", response_model=List[Progress], tags=["Progress"])
async def get_user_progress(user_id: str):
    """ 
    Retrieve progress entries for a specific user by user ID.
    """
    # Fetch progress entries for the given user ID
    progress = await get_progress_by_user_id(user_id)
    if not progress:
        raise HTTPException(status_code=404, detail="No progress entries found for user with the specified ID.")
    return progress

@router.get("/progress/{progress_id}", response_model=Progress, tags=["Progress"])
async def get_progress(progress_id: str):
    """ 
    Retrieve a single progress entry by its ID. 
    """
    # Fetch the progress entry by its ID
    progress = await get_progress_by_id(progress_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Progress entry with the specified ID not found. Please verify the progress ID.")
    return progress

@router.put("/progress/{progress_id}", response_model=Progress, tags=["Progress"])
async def update_progress_endpoint(progress_id: str, progress: ProgressCreate):
    """ 
    Update an existing progress entry by its ID.
    """
    # Check if the progress entry exists
    existing_progress = await get_progress_by_id(progress_id)
    if not existing_progress:
        raise HTTPException(status_code=404, detail="Progress entry with the specified ID not found. Unable to update.")
    
    # Update and return the progress entry
    updated_progress = await update_progress(progress_id, progress)
    if not updated_progress:
        raise HTTPException(status_code=500, detail="An error occurred while updating the progress entry. Please try again later.")

    return updated_progress

@router.delete("/progress/{progress_id}", response_model=dict, tags=["Progress"])
async def delete_progress_endpoint(progress_id: str):
    """ 
    Delete a progress entry by its ID.
    """
    # Attempt to delete the progress entry
    deleted = await delete_progress(progress_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Progress entry with the specified ID not found. Unable to delete.")
    
    return {"message": "Progress entry successfully deleted."}
