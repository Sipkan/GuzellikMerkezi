


from urllib.parse import urlparse

import asyncpg
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings
from app.db_models import Base

engine = create_async_engine(
    settings.database_url,
    echo=False,  # Disable SQL logging in production (prevents sensitive data in logs)
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


def _get_connection_params():
    """Parse DATABASE_URL into asyncpg connection params."""
    parsed = urlparse(settings.database_url.replace("postgresql+asyncpg://", "postgresql://"))
    return {
        "host": parsed.hostname or "localhost",
        "port": parsed.port or 5432,
        "user": parsed.username or "postgres",
        "password": parsed.password or "",
        "database": parsed.path.lstrip("/") if parsed.path else "postgres",
    }


async def _ensure_database_exists() -> None:
    """Create the database if it does not exist."""
    params = _get_connection_params()
    db_name = params.pop("database")

    if db_name == "postgres":
        return

    conn = await asyncpg.connect(database="postgres", **params)
    try:
        exists = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = $1", db_name
        )
        if not exists:
            await conn.execute(f'CREATE DATABASE "{db_name}"')
    finally:
        await conn.close()


async def init_db() -> None:
    """Create database if needed, then create all tables."""
    await _ensure_database_exists()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    """Dependency for getting a database session."""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
