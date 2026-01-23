# This file handles database setup, connection and session management for the Tweety app.
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine
import logging
from typing import AsyncGenerator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.exc import SQLAlchemyError
from fastapi import FastAPI
from sqlmodel import SQLModel
from sqlalchemy import text

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)  # Adjust level for prod


class Settings(BaseSettings):
    db_url: str
    db_pool_size: int = 10  # how many connections at a time
    db_pool_recycle: int = 3600  # Seconds before recycling connections
    db_echo: bool = False  # SQL logging, set to True for dev via DB_ECHO

    model_config = SettingsConfigDict(
        env_file=".env",  # Yeh bataata hai ki .env file se load karo
        env_prefix="",  # No prefix, use DB_URL directly
        case_sensitive=False,
    )


settings = Settings()


# Create async engine with production configs
engine: AsyncEngine = create_async_engine(
    settings.db_url,
    pool_size=settings.db_pool_size,
    pool_recycle=settings.db_pool_recycle,
    echo=settings.db_echo,
    pool_pre_ping=True,  # Check connections before use to avoid stale ones
)


async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            async with session.begin():
                yield session
        except SQLAlchemyError as err:
            logger.error(f"Database session error: {err}")
            await session.rollback()  # Explicit rollback on error
            raise  # Re-raise for FastAPI to handle
        except Exception as e:
            logger.error(f"Unexpected error in session: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()  # Ensure closure


async def create_db_tables():
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)


# FastAPI lifespan for startup/shutdown
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    try:
        await create_db_tables()
        logger.info("Database connected successfully 🚀")
        yield
    except Exception as e:
        logger.critical(f"Failed to connect to database: {e}")
        raise  # Prevent app start if DB fails
    finally:
        await engine.dispose()  # Clean up engine on shutdown
        logger.info("Database engine disposed")
