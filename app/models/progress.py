from pydantic import BaseModel, Field
from bson import ObjectId
from app.database import progress_collection
from typing import Dict, List, Optional

class ProgressBase(BaseModel):
    """ Base model representing the common attributes of a progress entry. """
    title: str
    content: str
    rating: int

    class Config:
        """ Pydantic configuration to allow certain behaviors in data handling. """
        arbitrary_types_allowed = True

class ProgressCreate(ProgressBase):
    """ Model used for creating a new progress entry. 
        Includes an alias for the user ID field.
    """
    user_id: str = Field(..., alias="userId")

class Progress(ProgressBase):
    """ Model representing a progress entry with additional attributes. """
    id: str
    user_id: str

    class Config:
        """ Pydantic configuration to support conversion from database attributes. """
        from_attributes = True

def progress_helper(progress) -> Dict[str, str]:
    """ Converts a MongoDB progress document into a dictionary.

    Args:
        progress (dict): The MongoDB progress document.

    Returns:
        dict: The progress data formatted for API responses.
    """
    return {
        "id": str(progress["_id"]),
        "title": progress["title"],
        "content": progress["content"],
        "rating": progress["rating"],
        "user_id": str(progress["user_id"]),
    }

async def create_progress(progress: ProgressCreate) -> Dict[str, str]:
    """ Creates a new progress entry in the database.

    Args:
        progress (ProgressCreate): The data for the new progress entry.

    Returns:
        dict: The created progress entry including its ID.

    Raises:
        Exception: If there is an error during the creation process.
    """
    try:
        progress_dict = progress.dict(by_alias=True)
        new_progress = await progress_collection.insert_one(progress_dict)
        created_progress = await progress_collection.find_one({"_id": new_progress.inserted_id})
        if created_progress:
            return progress_helper(created_progress)
        raise Exception("Failed to retrieve the created progress entry.")
    except Exception as e:
        raise Exception(f"Error creating progress: {str(e)}")

async def get_progress_by_user_id(user_id: str) -> List[Dict[str, str]]:
    """ Retrieves progress entries associated with a specific user ID.

    Args:
        user_id (str): The ID of the user whose progress entries to retrieve.

    Returns:
        List[dict]: A list of progress entries for the specified user.

    Raises:
        Exception: If there is an error retrieving progress entries.
    """
    try:
        progress_entries = await progress_collection.find({"user_id": ObjectId(user_id)}).to_list(length=None)
        return [progress_helper(progress) for progress in progress_entries]
    except Exception as e:
        raise Exception(f"Error retrieving progress for user ID {user_id}: {str(e)}")

async def get_progress_by_id(progress_id: str) -> Optional[Dict[str, str]]:
    """ Retrieves a single progress entry by its ID.

    Args:
        progress_id (str): The ID of the progress entry to retrieve.

    Returns:
        dict or None: The progress entry if found, otherwise None.

    Raises:
        Exception: If there is an error retrieving the progress entry.
    """
    try:
        progress = await progress_collection.find_one({"_id": ObjectId(progress_id)})
        if progress:
            return progress_helper(progress)
        return None
    except Exception as e:
        raise Exception(f"Error retrieving progress by ID {progress_id}: {str(e)}")

async def update_progress(progress_id: str, progress_data: ProgressCreate) -> Optional[Dict[str, str]]:
    """ Updates an existing progress entry with new data.

    Args:
        progress_id (str): The ID of the progress entry to update.
        progress_data (ProgressCreate): The updated progress data.

    Returns:
        dict or None: The updated progress entry if successful, otherwise None.

    Raises:
        Exception: If there is an error updating the progress entry.
    """
    try:
        update_data = progress_data.dict(by_alias=True, exclude_unset=True)
        existing_progress = await progress_collection.find_one({"_id": ObjectId(progress_id)})

        if not existing_progress:
            return None

        await progress_collection.update_one({"_id": ObjectId(progress_id)}, {"$set": update_data})
        updated_progress = await progress_collection.find_one({"_id": ObjectId(progress_id)})
        return progress_helper(updated_progress)
    except Exception as e:
        raise Exception(f"Error updating progress with ID {progress_id}: {str(e)}")

async def delete_progress(progress_id: str) -> bool:
    """ Deletes a progress entry by its ID.

    Args:
        progress_id (str): The ID of the progress entry to delete.

    Returns:
        bool: True if the progress entry was successfully deleted, otherwise False.

    Raises:
        Exception: If there is an error deleting the progress entry.
    """
    try:
        delete_result = await progress_collection.delete_one({"_id": ObjectId(progress_id)})
        return delete_result.deleted_count > 0
    except Exception as e:
        raise Exception(f"Error deleting progress with ID {progress_id}: {str(e)}")
