import logging
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Manages application environment variables securely using Pydantic.

    This class loads environment variables automatically from a .env file or
    from system environment variables. It enforces type checking and prevents
    hardcoded secrets across the codebase.
    """

    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    APP_PORT: int = 8000
    DATABASE_URL: str = "sqlite:///./tasks.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


def setup_logging(log_level: str) -> None:
    """Configures structured stream logging for the entire application.

    Args:
        log_level (str): The logging severity level (e.g., 'INFO', 'DEBUG').

    Returns:
        None
    """
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


# Instantiate settings instance to be imported across the app
settings = Settings()
setup_logging(settings.LOG_LEVEL)
