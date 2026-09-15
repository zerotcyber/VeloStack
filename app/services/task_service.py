import logging
from typing import Sequence
from fastapi import HTTPException, status
from app.repositories.task_repo import TaskRepository
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate

logger = logging.getLogger(__name__)


class TaskService:
    """Handles business logic operations for Task management."""

    def __init__(self, task_repo: TaskRepository) -> None:
        """Initializes service with a task repository dependency.

        Args:
            task_repo (TaskRepository): Repository handling data access.
        """
        self.task_repo = task_repo

    def get_task(self, task_id: int) -> TaskResponse:
        """Retrieves a single task by ID or raises HTTP 404.

        Args:
            task_id (int): Primary key identifier of task.

        Returns:
            TaskResponse: Validated output schema.

        Raises:
            HTTPException: 404 error if task is not found.
        """
        task = self.task_repo.get_by_id(task_id)
        if not task:
            logger.warning("Task with ID %s requested but not found.", task_id)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID {task_id} does not exist.",
            )
        return TaskResponse.model_validate(task)

    def list_tasks(self, skip: int = 0, limit: int = 100) -> Sequence[TaskResponse]:
        """Retrieves a list of tasks with pagination.

        Args:
            skip (int): Number of records to skip.
            limit (int): Maximum records to fetch.

        Returns:
            Sequence[TaskResponse]: List of validated response schemas.
        """
        tasks = self.task_repo.get_all(skip=skip, limit=limit)
        return [TaskResponse.model_validate(t) for t in tasks]

    def create_task(self, schema: TaskCreate) -> TaskResponse:
        """Creates a new task.

        Args:
            schema (TaskCreate): Input creation payload.

        Returns:
            TaskResponse: Newly created task response.
        """
        task = self.task_repo.create(schema)
        logger.info("Created new task with ID %s", task.id)
        return TaskResponse.model_validate(task)

    def update_task(self, task_id: int, schema: TaskUpdate) -> TaskResponse:
        """Updates an existing task or raises HTTP 404.

        Args:
            task_id (int): ID of task to update.
            schema (TaskUpdate): Fields to update.

        Returns:
            TaskResponse: Updated task object.

        Raises:
            HTTPException: 404 error if task to update does not exist.
        """
        task = self.task_repo.update(task_id, schema)
        if not task:
            logger.warning("Attempted to update non-existent task ID %s.", task_id)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID {task_id} does not exist.",
            )
        logger.info("Updated task ID %s", task_id)
        return TaskResponse.model_validate(task)

    def delete_task(self, task_id: int) -> None:
        """Removes a task by ID or raises HTTP 404.

        Args:
            task_id (int): ID of task to delete.

        Raises:
            HTTPException: 404 error if task does not exist.
        """
        success = self.task_repo.delete(task_id)
        if not success:
            logger.warning("Attempted to delete non-existent task ID %s.", task_id)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID {task_id} does not exist.",
            )
        logger.info("Deleted task ID %s", task_id)
