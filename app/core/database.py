"""
Database configuration and session management.

This module provides the SQLAlchemy engine, session factory,
and base class for all database models.
"""

from typing import AsyncGenerator, Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from app.core.config import settings

# ==================== Sync Database Setup ====================
# For Alembi migrations and synchronous operations

# Create synchronous engine
sync_engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    pool_pre_ping=True,  # Verify connections before using them
    pool_size=5,  # Max number of connections to keep in pool
    max_overflow=10,  # Max connections beyond pool_size
)

# Create synchronous session factory
SyncSessionFactory = sessionmaker(
    autocommit=False,  # Commit transactions at the end of the request
    autoflush=False,  # Flush changes to the database after each statement
    bind=sync_engine,  # Bind the session to the engine
)


# ==================== Async Database Setup ====================
# For async FastAPI endpoints

# Create async engine
async_engine = create_async_engine(
    settings.database_url_async,  # Async PostgreSQL connection URL
    echo=settings.DATABASE_ECHO,  # Enable SQLAlchemy query logging
    pool_pre_ping=True,  # Verify connections before using them
    pool_size=5,  # Max number of connections to keep in pool
    max_overflow=10,  # Max connections beyond pool_size
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    async_engine,  # Bind the session to the engine
    class_=AsyncSession,  # Use AsyncSession class
    expire_on_commit=False,  # Keep objects in memory after commit
    autocommit=False,  # Commit transactions at the end of the request
    autoflush=False,  # Flush changes to the database after each statement
)

# ==================== Base Model ====================
# All database models will inherit from this base class

Base = declarative_base()  # Create base class for all models

# ==================== Database Dependencies ====================


def get_sync_db() -> Generator[Session, None, None]:
    """
    Dependency for synchronous database sessions.

    Provides a database session that automatically commits or rolls back
    on completion. Used with synchronous code and Alembic migrations.
    """
    db = SyncSessionFactory()  # Create a new session
    try:
        yield db  # Yield the session to the caller
        db.commit()  # Commit the transaction
    except Exception:
        db.rollback()  # Roll back the transaction
        raise
    finally:
        db.close()  # Close the session


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for asynchronous database sessions.

    Provides an async database session for use with async endpoints.
    Automatically handles commits and rollbacks.

    Yields:
        AsyncSession: Async SQLAlchemy database session

    Example:
        >>> @app.get("/users")
        >>> async def get_users(db: AsyncSession = Depends(get_async)db)):
        ...     users = await db.execute(select(User))
        ...     return users.scalars().all()
    Raises:
        Exception: If an error occurs during the session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session  # Yield the session to the caller
            await session.commit()  # Commit the transaction
        except Exception:
            await session.rollback()  # Roll back the transaction
            raise
        finally:
            await session.close()  # Close the session


# ==================== Database Utilities ====================


async def init_db() -> None:
    """
    Initialize the database.

    Creates all tables defined in SQLAlchemy models.
    This should only be used in development. In production,
    use Alembic migrations instead.

    Example:
        >>> import asyncio
        >>> asyncio.run(init_db())
    """
    async with async_engine.begin() as conn:
        # Import all models here to ensure they are registered with SQLAlchemy
        from app.models import user  # noqa: F401

        # Create all tables
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """
    Close database connections.

    Should be caled on application shutdown to properly
    close all database connections.

    Example:
        >>> @app.on_event("shutdown")
        >>> async def shutdown_event():
        ...     await close_db()
    """
    await async_engine.dispose()  # Close all connections in the pool
