from pydantic import BaseModel
from bson.objectid import ObjectId
from app.database import milestones_collection
from typing import Dict, List, Optional

"""
Milestones module
"""

class MilestonesBase(BaseModel):
    """ Base model for milestones, containing common attributes. """
    project_item: str
    quantity: int

class MilestonesCreate(MilestonesBase):
    """ Model used for creating a new milestone.
        Includes additional fields for project and task identifiers.
    """
    project_id: str
    task_id: str

class Milestones(MilestonesBase):
    """ Model representing a milestone with identifiers. """
    id: str
    project_id: str
    task_id: str

    class Config:
        """ Pydantic configuration to enable conversion from MongoDB document attributes. """
        from_attributes = True

def milestones_helper(milestones) -> Dict[str, str]:
    """ Converts a MongoDB milestone document into a dictionary.

    Args:
        milestones (dict): The MongoDB milestone document.

    Returns:
        dict: A dictionary representation of the milestone, suitable for API responses.
    """
    return {
        "id": str(milestones["_id"]),
        "project_item": milestones["project_item"],
        "quantity": milestones["quantity"],
        "project_id": milestones["project_id"],
        "task_id": milestones["task_id"],
    }

async def create_milestones(milestones: MilestonesCreate) -> Dict[str, str]:
    """ Creates a new milestone and returns its details.

    Args:
        milestones (MilestonesCreate): The data to create the new milestone.

    Returns:
        dict: The created milestone with its ID.

    Raises:
        Exception: If there is an error creating the milestone or retrieving it.
    """
    try:
        milestones_dict = milestones.dict()
        new_milestone = await milestones_collection.insert_one(milestones_dict)
        created_milestone = await milestones_collection.find_one({"_id": new_milestone.inserted_id})
        if created_milestone:
            return milestones_helper(created_milestone)
        raise Exception("Failed to retrieve the created milestone.")
    except Exception as e:
        raise Exception(f"Error creating milestone: {str(e)}")

async def get_milestoness(skip: int = 0, limit: int = 10) -> List[Dict[str, str]]:
    """ Retrieves a list of milestones with pagination.

    Args:
        skip (int): The number of milestones to skip.
        limit (int): The maximum number of milestones to return.

    Returns:
        List[dict]: A list of milestones with their details.

    Raises:
        Exception: If there is an error retrieving the milestones.
    """
    try:
        milestones_list = await milestones_collection.find().skip(skip).limit(limit).to_list(length=limit)
        return [milestones_helper(milestone) for milestone in milestones_list]
    except Exception as e:
        raise Exception(f"Error retrieving milestones: {str(e)}")

async def get_milestones_by_id(id: str) -> Optional[Dict[str, str]]:
    """ Retrieves a single milestone by its ID.

    Args:
        id (str): The ID of the milestone to retrieve.

    Returns:
        dict or None: The milestone if found, otherwise None.

    Raises:
        Exception: If there is an error retrieving the milestone.
    """
    try:
        milestone = await milestones_collection.find_one({"_id": ObjectId(id)})
        if milestone:
            return milestones_helper(milestone)
        return None
    except Exception as e:
        raise Exception(f"Error retrieving milestone by ID {id}: {str(e)}")

async def delete_milestones(id: str) -> bool:
    """ Deletes a milestone by its ID.

    Args:
        id (str): The ID of the milestone to delete.

    Returns:
        bool: True if the milestone was deleted, otherwise False.

    Raises:
        Exception: If there is an error deleting the milestone.
    """
    try:
        delete_result = await milestones_collection.delete_one({"_id": ObjectId(id)})
        return delete_result.deleted_count > 0
    except Exception as e:
        raise Exception(f"Error deleting milestone with ID {id}: {str(e)}")

async def update_milestones(id: str, milestones_data: MilestonesBase) -> Optional[Dict[str, str]]:
    """ Updates a milestone with new data.

    Args:
        id (str): The ID of the milestone to update.
        milestones_data (MilestonesBase): The new data for the milestone.

    Returns:
        dict or None: The updated milestone if successful, otherwise None.

    Raises:
        Exception: If there is an error updating the milestone or retrieving the updated data.
    """
    try:
        updated_data = milestones_data.dict(exclude_unset=True)
        update_result = await milestones_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": updated_data}
        )
        if update_result.modified_count > 0:
            return await get_milestones_by_id(id)
        return None
    except Exception as e:
        raise Exception(f"Error updating milestone with ID {id}: {str(e)}")

async def get_milestoness_by_project_id(project_id: str, skip: int = 0, limit: int = 10) -> List[Dict[str, str]]:
    """ Retrieves a list of milestones associated with a specific project ID.

    Args:
        project_id (str): The ID of the project whose milestones to retrieve.
        skip (int): The number of milestones to skip.
        limit (int): The maximum number of milestones to return.

    Returns:
        List[dict]: A list of milestones associated with the specified project.

    Raises:
        Exception: If there is an error retrieving the milestones.
    """
    try:
        milestones_list = await milestones_collection.find({"project_id": project_id}).skip(skip).limit(limit).to_list(length=limit)
        return [milestones_helper(milestone) for milestone in milestones_list]
    except Exception as e:
        raise Exception(f"Error retrieving milestones for project ID {project_id}: {str(e)}")
