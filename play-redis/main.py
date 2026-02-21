from fastapi import FastAPI
import httpx


app = FastAPI()


@app.get("/")
async def fetch_random_data():
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get("https://jsonplaceholder.typicode.com/todos")
            return res.json()
    except Exception as err:
        print(f"error while fetch data: {err}")
