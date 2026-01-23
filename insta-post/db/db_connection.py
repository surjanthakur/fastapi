from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker ,AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
import logging
from sqlmodel import SQLModel
from typing import AsyncGenerator
from pydantic_settings import BaseSettings ,SettingsConfigDict
from sqlalchemy.exc import SQLAlchemyError


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class Settings(BaseSettings):
    db_url:str
    db_pool_size:int = 10
    db_pool_recycle:int = 3600
    db_echo:bool = False

    model_config  = SettingsConfigDict(
         env_file=".env",
         env_file_encoding='utf-8'
    )

setting = Settings()

engine: AsyncEngine = create_async_engine(
    setting.db_url,
    pool_size=setting.db_pool_size,
    pool_recycle=setting.db_pool_recycle,
    echo=setting.db_echo,
    pool_pre_ping=True,

)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    try:
     async with async_session_maker() as session:
        yield session
    except SQLAlchemyError as err:
       logger.error(f"database session error: {err}")
       await session.rollback()
       raise
    except Exception as err:
       logger.error(f"session failed,something went wrong with get_session: {err}")
       await session.rollback()
       raise
    finally:
       await session.close() # Ensure close every session completion.
       


async def create_db_tables():
    try:
     async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    except SQLAlchemyError as err:
        logger.error(f"database table creation error: {err}")
        raise
    except Exception as err:
        logger.error(f"table creation failed,something went wrong: {err}")



       
