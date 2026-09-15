from typing import Sequence
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.repositories.task_repo import TaskRepository
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])


def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    """Dependency provider for TaskService.

    Args:
        db (Session): Database session injected by FastAPI.

    Returns:
        TaskService: Service instance initialized with repository.
    """
    repo = TaskRepository(db)
    return TaskService(repo)


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
)
def create_task(
    payload: TaskCreate,
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    """Creates a new task in the database."""
    return service.create_task(payload)


@router.get(
    "/",
    response_model=Sequence[TaskResponse],
    status_code=status.HTTP_200_OK,
    summary="List all tasks",
)
def list_tasks(
    skip: int = 0,
    limit: int = 100,
    service: TaskService = Depends(get_task_service),
) -> Sequence[TaskResponse]:
    """Retrieves a paginated list of tasks."""
    return service.list_tasks(skip=skip, limit=limit)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Get task by ID",
)
def get_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    """Retrieves details of a specific task."""
    return service.get_task(task_id)


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Update task partially",
)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    """Updates attributes of an existing task."""
    return service.update_task(task_id, payload)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
)
def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
) -> None:
    """Deletes a task by identifier."""
    service.delete_task(task_id)
