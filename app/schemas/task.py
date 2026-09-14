from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class TaskBase(BaseModel):
    """Base schema holding common fields for Task entities.

    Attributes:
        title (str): Short name or summary of the task.
        description (Optional[str]): Detailed explanation of the task.
    """

    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="The main summary title of the task.",
        examples=["Complete Dockerfile configuration"],
    )
    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Optional detailed notes about the task.",
        examples=["Implement multi-stage build pattern with non-root user."],
    )


class TaskCreate(TaskBase):
    """Schema representing the input payload required to create a new task.

    Inherits all fields from TaskBase without modification.
    """

    pass


class TaskUpdate(BaseModel):
    """Schema representing the input payload to update an existing task.

    All fields are optional to allow partial updates (PATCH operations).
    """

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="Updated title of the task.",
    )
    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Updated description of the task.",
    )
    is_completed: Optional[bool] = Field(
        default=None,
        description="Status flag indicating whether the task is finished.",
    )


class TaskResponse(TaskBase):
    """Schema representing the output payload returned in API responses.

    Attributes:
        id (int): Unique database auto-incrementing identifier.
        is_completed (bool): True if completed, False otherwise.
        created_at (datetime): Timestamp when the record was created.
        updated_at (datetime): Timestamp when the record was last modified.
    """

    id: int = Field(
        ...,
        description="Unique database primary key identifier.",
    )
    is_completed: bool = Field(
        ...,
        description="Completion state of the task.",
    )
    created_at: datetime = Field(
        ...,
        description="UTC timestamp of task creation.",
    )
    updated_at: datetime = Field(
        ...,
        description="UTC timestamp of last task modification.",
    )

    model_config = ConfigDict(from_attributes=True)
