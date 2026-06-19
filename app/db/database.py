from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings
import os

# Create engine with SQLite configuration
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
    echo=False,
)


def create_db_and_tables() -> None:
    """Create database tables."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    """Get a database session."""
    return Session(engine)


class Database:
    """Database management class for SQLModel operations."""

    def __init__(self):
        """Initialize database instance."""
        self.db_url = settings.database_url
        self.engine = engine

    def connect(self) -> None:
        """Establish database connection and create tables."""
        os.makedirs("app/db", exist_ok=True)
        create_db_and_tables()

    def close(self) -> None:
        """Close database connection."""
        if self.engine:
            self.engine.dispose()

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# Shared database instance used across the app
db = Database()
