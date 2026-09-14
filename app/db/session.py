from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from app.core.config import settings

# Create SQLAlchemy Database Engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
)

# Factory for creating new database session instances
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base class for SQLAlchemy ORM models to inherit from
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Provides a transactional database session context manager.

    Yields:
        Session: Active SQLAlchemy session instance.

    Ensures that the connection is closed automatically after request completion,
    preventing connection leaks in production pools.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
