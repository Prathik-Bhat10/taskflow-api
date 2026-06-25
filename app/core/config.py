"""Application configuration loaded from environment variables / .env file."""
from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import quote_plus


class Settings(BaseSettings):
    app_name: str = "TaskFlow API"
    app_version: str = "1.0.0"
    debug: bool = False
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "taskflow_db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def POSTGRES_URL(self) -> str:
        """Construct the PostgreSQL database URL."""
        user = quote_plus(self.POSTGRES_USER)
        password = quote_plus(self.POSTGRES_PASSWORD)
        database = quote_plus(self.POSTGRES_DB)
        return (
            f"postgresql+asyncpg://{user}:{password}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{database}"
        )


settings = Settings()
