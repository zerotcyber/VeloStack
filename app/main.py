import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Dict
from fastapi import FastAPI
from app.api.v1.tasks import router as task_router
from app.core.config import settings
from app.db.session import Base, engine

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manages application startup and shutdown lifecycle events.

    Args:
        app (FastAPI): The application instance.
    """
    logger.info("Initializing database schema on startup...")
    Base.metadata.create_all(bind=engine)
    logger.info("Application startup complete.")
    yield
    logger.info("Application shutting down...")


app = FastAPI(
    title="Task Management API",
    description="Production-grade FastAPI REST service containerized with Docker.",
    version="1.0.0",
    lifespan=lifespan,
)

# Register API v1 Routers
app.include_router(task_router, prefix="/api/v1")


@app.get("/health", tags=["Health"])
def health_check() -> Dict[str, str]:
    """Healthcheck endpoint for container orchestration engines (Docker/K8s)."""
    return {"status": "healthy", "environment": settings.ENVIRONMENT}
