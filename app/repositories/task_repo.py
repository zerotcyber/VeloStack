from typing import Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.task import TaskModel
from app.schemas.task import TaskCreate, TaskUpdate


class TaskRepository:
    """Encapsulates all database operations for Task entities."""

    def __init__(self, db: Session) -> None:
        """Initializes the repository with an active database session.

        Args:
            db (Session): Active SQLAlchemy database session.
        """
        self.db = db

    def get_by_id(self, task_id: int) -> TaskModel | None:
        """Retrieves a single task record by primary key ID.

        Args:
            task_id (int): The ID of the task to retrieve.

        Returns:
            TaskModel | None: Found task instance or None if not found.
        """
        stmt = select(TaskModel).where(TaskModel.id == task_id)
        return self.db.scalars(stmt).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[TaskModel]:
        """Retrieves a paginated collection of task records.

        Args:
            skip (int): Number of records to skip for pagination.
            limit (int): Maximum number of records to return.

        Returns:
            Sequence[TaskModel]: List of task ORM instances.
        """
        stmt = select(TaskModel).offset(skip).limit(limit)
        return self.db.scalars(stmt).all()

    def create(self, schema: TaskCreate) -> TaskModel:
        """Persists a new task entity into the database.

        Args:
            schema (TaskCreate): Validated Pydantic creation schema.

        Returns:
            TaskModel: Saved ORM entity containing generated ID and timestamps.
        """
        db_task = TaskModel(
            title=schema.title,
            description=schema.description,
        )
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def update(self, task_id: int, schema: TaskUpdate) -> TaskModel | None:
        """Updates an existing task entity in the database.

        Args:
            task_id (int): Identifier of task to update.
            schema (TaskUpdate): Validated Pydantic update schema containing fields.

        Returns:
            TaskModel | None: Updated task instance, or None if task was not found.
        """
        db_task = self.get_by_id(task_id)
        if not db_task:
            return None

        update_data = schema.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value)

        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def delete(self, task_id: int) -> bool:
        """Removes a task entity from the database.

        Args:
            task_id (int): Identifier of task to remove.

        Returns:
            bool: True if task was successfully deleted, False if not found.
        """
        db_task = self.get_by_id(task_id)
        if not db_task:
            return False

        self.db.delete(db_task)
        self.db.commit()
        return True
