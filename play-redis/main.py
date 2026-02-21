from fastapi import FastAPI
import axios
import json


router = FastAPI()


@router.get("/")
async def fetch_random_data():
    try:
        res = await axios.get("https://jsonplaceholder.typicode.com/todos")
        return json(res)
    except Exception as err:
        print(f"error while fetch data: {err}")
