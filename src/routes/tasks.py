from fastapi import APIRouter, Depends

from src.dependencies.task import get_task_service
from src.schemas.task import TaskCreate, TaskGet
from src.services.task import TaskService
from src.dependencies.auth import get_current_user

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)

@router.get("/", response_model=list[TaskGet])
async def get_tasks(
    task_service: TaskService = Depends(get_task_service),
    current_user = Depends(get_current_user)
):
    return task_service.get_all(user_id=current_user.id)

@router.get("/all", response_model=list[TaskGet])
def get_all_tasks(task_service: TaskService = Depends(get_task_service), current_user = Depends(get_current_user)):
    return task_service.get_all_tasks(role=current_user.role)

@router.get("/sorted", response_model=list[TaskGet])
def get_sorted_tasks(
    task_service: TaskService = Depends(get_task_service),
    current_user = Depends(get_current_user)
):
    tasks = task_service.get_all(user_id=current_user.id)
    return sorted(tasks, key=lambda t: t.priority)

@router.post("/", response_model=TaskGet)
def create_task(
    task: TaskCreate,
    task_service: TaskService = Depends(get_task_service),
    current_user = Depends(get_current_user)
):
    return task_service.create_task(task.model_dump(), user_id=current_user.id)

@router.patch("/{task_id}/done", response_model=TaskGet)
def mark_done(
    task_id: int,
    task_service: TaskService = Depends(get_task_service),
    current_user = Depends(get_current_user)
):
    return task_service.mark_done(task_id, user_id=current_user.id)

@router.patch("/{task_id}/priority", response_model=TaskGet)
def change_priority(
    task_id: int,
    new_priority: int,
    task_service: TaskService = Depends(get_task_service),
    current_user = Depends(get_current_user)
):
    return task_service.change_priority(task_id, new_priority, user_id=current_user.id)

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    task_service: TaskService = Depends(get_task_service),
    current_user = Depends(get_current_user)
):
    success = task_service.delete_task(task_id, user_id=current_user.id, role=current_user.role)
    return {"deleted": success}