from fastapi import FastAPI
from db.db_connection import create_db_tables
from contextlib import asynccontextmanager
from router import user, profile


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_tables()
    print("database created successfully 🚀!")
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(router=user.user_router)
app.include_router(router=profile.profile_router)
