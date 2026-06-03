from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "TaskFlow API"
    app_version: str = "1.0.0"
    debug: bool = True
    secret_key: str = "changeme"
    database_url: str = "postgresql://postgres:password@localhost:5432/taskflow"

    class Config:
        env_file = ".env"

settings = Settings()