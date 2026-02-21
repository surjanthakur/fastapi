from fastapi import FastAPI
import httpx
import redis
import json


rds = redis.Redis(port=6379, host="localhost", db=0, decode_responses=True)

CACHE_KEY = "todos_cache"
CACHE_EXPIRY = 60  # 1 minute


app = FastAPI()


@app.get("/")
async def fetch_random_data():
    cache_data = rds.get(CACHE_KEY)
    if cache_data:
        print("Returning data from cache...")
        return json.loads(cache_data)
    try:
        print("Fetching data from API...")
        async with httpx.AsyncClient() as client:
            res = await client.get("https://jsonplaceholder.typicode.com/todos")
            todos = res.json()
            rds.setex(CACHE_KEY, CACHE_EXPIRY, json.dumps(todos))
            return todos
    except Exception as err:
        print(f"error while fetch data: {err}")
