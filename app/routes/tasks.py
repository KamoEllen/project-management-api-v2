from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.tasks import Tasks, TasksCreate, TasksBase
from app.routes.auth import get_current_user
from app.models.user import User

router = APIRouter()

# Static data for demonstration
STATIC_PROJECT_ID = "nhdyrsWGRkkutte343"
STATIC_TASK_ID = "sBKdsLnc7251Gs"


TASK_DATA = {
    STATIC_TASK_ID: {
        "id": STATIC_TASK_ID,
        "project_id": STATIC_PROJECT_ID,
        "task_description": "example_task_description",
        "user_id": "example_user_id"
    }
}

@router.post("/tasks/", response_model=Tasks, tags=["Tasks"])
async def create_tasks_endpoint(task: TasksCreate, current_user: User = Depends(get_current_user)):
    """
    Create a new task with static task ID and project ID.
    """
    # For demo purposes, using static task ID and project ID
    new_task = {
        "id": STATIC_TASK_ID,
        "project_id": STATIC_PROJECT_ID,
        "task_description": task.task_description,
        "user_id": current_user["id"]
    }
    # Update the static data store
    TASK_DATA[STATIC_TASK_ID] = new_task
    return new_task

@router.get("/tasks/", response_model=List[Tasks], tags=["Tasks"])
async def get_tasks_endpoint(skip: int = 0, limit: int = 10):
    """
    Retrieve a paginated list of tasks with static data.
    """
    # Generate a list of tasks based on the static data
    tasks = list(TASK_DATA.values())
    return tasks[skip:skip + limit]

@router.get("/tasks/{id}", response_model=Tasks, tags=["Tasks"])
async def get_task_endpoint(id: str):
    """
    Retrieve a single task by its ID with static data.
    """
    task = TASK_DATA.get(id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{id}", response_model=Tasks, tags=["Tasks"])
async def update_task_endpoint(id: str, task_data: TasksBase, current_user: User = Depends(get_current_user)):
    """
    Update a task by its ID with static data.
    """
    if id not in TASK_DATA:
        raise HTTPException(status_code=404, detail="Task not found")
    
    updated_task = {
        "id": id,
        "project_id": STATIC_PROJECT_ID,
        "task_description": task_data.task_description,
        "user_id": current_user["id"]
    }
    TASK_DATA[id] = updated_task
    return updated_task

@router.delete("/tasks/{id}", response_model=dict, tags=["Tasks"])
async def delete_task_endpoint(id: str, current_user: User = Depends(get_current_user)):
    """
    Delete a task by its ID.
    """
    if id not in TASK_DATA:
        raise HTTPException(status_code=404, detail="Task not found")
    
    del TASK_DATA[id]
    return {"message": "Task deleted successfully"}


#----- works but will use static ID for demo
# from fastapi import APIRouter, Depends, HTTPException
# from typing import List
# from app.models.tasks import Tasks, TasksCreate, TasksBase, create_tasks, get_tasks, get_tasks_by_id, update_tasks, delete_tasks
# from app.routes.auth import get_current_user
# from app.models.user import User

# router = APIRouter()

# @router.post("/tasks/", response_model=dict, tags=["Tasks"])
# async def create_tasks_endpoint(task: TasksCreate, current_user: User = Depends(get_current_user)):
#     """ 
#     Create a new task. 
#     """
#     task = await create_tasks(task, user_id=current_user["id"])
#     return {"task_id": task.id}

# @router.get("/tasks/", response_model=List[Tasks], tags=["Tasks"])
# async def get_tasks_endpoint(skip: int = 0, limit: int = 10):
#     """ 
#     Retrieve a paginated list of tasks.
#     """
#     tasks = await get_tasks(skip=skip, limit=limit)
#     return tasks

# @router.get("/tasks/{id}", response_model=Tasks, tags=["Tasks"])
# async def get_task_endpoint(id: str):
#     """ 
#     Retrieve a single task by its ID.
#     """
#     task = await get_tasks_by_id(id)
#     if task is None:
#         raise HTTPException(status_code=404, detail="Task not found")
#     return task

# @router.put("/tasks/{id}", response_model=Tasks, tags=["Tasks"])
# async def update_task_endpoint(id: str, task_data: TasksBase, current_user: User = Depends(get_current_user)):
#     """ 
#     Update a task by its ID.
#     """
#     # Fetch the existing task
#     existing_task = await get_tasks_by_id(id)
#     if existing_task is None:
#         raise HTTPException(status_code=404, detail="Task not found")
    
#     # Check if the current user is the owner of the task
#     if existing_task.user_id != current_user["id"]:
#         raise HTTPException(status_code=403, detail="Not authorized to update this task")
    
#     # Update the task
#     updated_task = await update_tasks(id, task_data)
#     if not updated_task:
#         raise HTTPException(status_code=404, detail="Failed to update task")
#     return updated_task

# @router.delete("/tasks/{id}", response_model=dict, tags=["Tasks"])
# async def delete_task_endpoint(id: str, current_user: User = Depends(get_current_user)):
#     """ 
#     Delete a task by its ID.
#     """
#     # Fetch the existing task
#     existing_task = await get_tasks_by_id(id)
#     if existing_task is None:
#         raise HTTPException(status_code=404, detail="Task not found")
    
#     # Check if the current user is the owner of the task
#     if existing_task.user_id != current_user["id"]:
#         raise HTTPException(status_code=403, detail="Not authorized to delete this task")
    
#     # Delete the task
#     deleted = await delete_tasks(id)
#     if not deleted:
#         raise HTTPException(status_code=404, detail="Task not found")
#     return {"message": "Task deleted successfully"}
