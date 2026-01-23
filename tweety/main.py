from fastapi import FastAPI
from database.database import lifespan
from router import users, tweets


app = FastAPI(lifespan=lifespan)

app.include_router(router=users.router)
app.include_router(router=tweets.tweet_router)
