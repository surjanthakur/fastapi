from fastapi import FastAPI
from db.db_connection import create_db_tables
from contextlib import asynccontextmanager
from router import user, profile
import logging

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await create_db_tables()
        print("database created successfully 🚀!")
        yield

    except Exception as e:
        logging.error(f"Error during database setup: {e}")


PRODUCTION = False

app = FastAPI(
    lifespan=lifespan,
    docs_url=None if PRODUCTION else "/docs",
    redoc_url=None if PRODUCTION else "/redoc",
    openapi_url=None if PRODUCTION else "/openapi.json",
)


app.include_router(router=user.user_router)
app.include_router(router=profile.profile_router)
