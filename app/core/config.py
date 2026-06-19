"""Application configuration loaded from environment variables / .env file."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "TaskFlow API"
    app_version: str = "1.0.0"
    debug: bool = False
    database_url: str = "sqlite:///app/db/sqlite3.db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
