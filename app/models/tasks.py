from pydantic import BaseModel
from typing import List, Optional, Dict
from uuid import uuid4

# Static data structure to simulate a database
TASK_DATA: Dict[str, Dict[str, str]] = {}

class TasksBase(BaseModel):
    """Base model for tasks with basic task attributes."""
    project_id: str
    task_description: str

class TasksCreate(TasksBase):
    """Model for creating a new task, inherits from TasksBase."""
    pass

class Tasks(TasksBase):
    """Model representing a task, including additional attributes for task management."""
    id: str
    user_id: str

    class Config:
        """Pydantic configuration for the Tasks model."""
        from_attributes = True

def tasks_helper(task: Dict[str, str]) -> dict:
    """Transforms a task dictionary into a dictionary suitable for API responses.

    Args:
        task (dict): The task dictionary.

    Returns:
        dict: Transformed task data suitable for API responses.
    """
    return {
        "id": task["id"],
        "project_id": task["project_id"],
        "task_description": task["task_description"],
        "user_id": task["user_id"],
    }

async def create_tasks(task: TasksCreate, user_id: str) -> dict:
    """Creates a new task and stores it in the static data structure.

    Args:
        task (TasksCreate): The task creation model containing task data.
        user_id (str): The ID of the user creating the task.

    Returns:
        dict: The created task data including its ID.

    Raises:
        Exception: If there's an error creating the task.
    """
    try:
        task_id = str(uuid4())
        task_dict = task.dict()
        task_dict['user_id'] = user_id
        task_dict['id'] = task_id
        TASK_DATA[task_id] = task_dict
        return tasks_helper(task_dict)
    except Exception as e:
        raise Exception(f"Error creating task: {str(e)}")

async def get_tasks(skip: int = 0, limit: int = 10) -> List[dict]:
    """Retrieves a list of tasks with pagination from the static data structure.

    Args:
        skip (int): Number of tasks to skip for pagination. Default is 0.
        limit (int): Maximum number of tasks to return. Default is 10.

    Returns:
        List[dict]: A list of tasks, each represented as a dictionary.

    Raises:
        Exception: If there's an error retrieving tasks.
    """
    try:
        tasks_list = list(TASK_DATA.values())
        return [tasks_helper(task) for task in tasks_list[skip:skip + limit]]
    except Exception as e:
        raise Exception(f"Error retrieving tasks: {str(e)}")

async def get_tasks_by_id(id: str) -> Optional[dict]:
    """Retrieves a single task by its ID from the static data structure.

    Args:
        id (str): The ID of the task to retrieve.

    Returns:
        dict or None: The task data if found, otherwise None.

    Raises:
        Exception: If there's an error retrieving the task.
    """
    try:
        task = TASK_DATA.get(id)
        if task:
            return tasks_helper(task)
        return None
    except Exception as e:
        raise Exception(f"Error retrieving task by ID: {str(e)}")

async def update_tasks(id: str, task_data: TasksBase) -> Optional[dict]:
    """Updates an existing task with new data in the static data structure.

    Args:
        id (str): The ID of the task to update.
        task_data (TasksBase): The new data to update the task with.

    Returns:
        dict or None: The updated task data if successful, otherwise None.

    Raises:
        Exception: If there's an error updating the task.
    """
    try:
        if id in TASK_DATA:
            updated_data = task_data.dict(exclude_unset=True)
            task = TASK_DATA[id]
            task.update(updated_data)
            return tasks_helper(task)
        return None
    except Exception as e:
        raise Exception(f"Error updating task: {str(e)}")

async def delete_tasks(id: str) -> bool:
    """Deletes a task by its ID from the static data structure.

    Args:
        id (str): The ID of the task to delete.

    Returns:
        bool: True if the task was successfully deleted, False otherwise.

    Raises:
        Exception: If there's an error deleting the task.
    """
    try:
        if id in TASK_DATA:
            del TASK_DATA[id]
            return True
        return False
    except Exception as e:
        raise Exception(f"Error deleting task: {str(e)}")
