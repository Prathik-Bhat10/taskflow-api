from typing import AsyncGenerator
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings

# Create engine with PostgreSQL configuration
engine = create_async_engine(
    settings.POSTGRES_URL,
    echo=True
)

# Create session factory
async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def create_db_and_tables() -> None:
    """Create database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get a database session."""
    async with async_session_maker() as session:
        yield session


class Database:
    """Database management class for SQLModel operations."""

    def __init__(self):
        """Initialize database instance."""
        self.db_url = settings.POSTGRES_URL
        self.engine = engine

    async def connect(self) -> None:
        """Establish database connection and create tables."""
        await create_db_and_tables()

    async def close(self) -> None:
        """Close database connection."""
        if self.engine:
            await self.engine.dispose()

    async def __aenter__(self):
        """Context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        await self.close()


# Shared database instance used across the app
db = Database()