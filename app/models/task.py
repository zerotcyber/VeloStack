from datetime import datetime, timezone
from sqlalchemy import String, Boolean, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base


def utc_now() -> datetime:
    """Helper returning timezone-aware current UTC time.

    Returns:
        datetime: Current timestamp in UTC timezone.
    """
    return datetime.now(timezone.utc)


class TaskModel(Base):
    """SQLAlchemy ORM model representing the 'tasks' database table.

    Attributes:
        id (int): Primary key database identifier.
        title (str): Short name/summary of task.
        description (str, optional): Detailed explanation of task.
        is_completed (bool): True if completed, False otherwise.
        created_at (datetime): Timestamp when record was created.
        updated_at (datetime): Timestamp when record was last modified.
    """

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )
