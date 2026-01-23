from fastapi import FastAPI, HTTPException, status, Path
from fastapi.responses import JSONResponse
import json
from pydantic_schema import User, User_update

app = FastAPI()


def load_data():
    with open("users.json", "r") as file:
        data = json.load(file)
    return data


def save_data(data):
    with open("users.json", "w") as file:
        json.dump(data, file)


# get all users
@app.get("/users")
def get_all_users():
    try:
        data = load_data()
        return JSONResponse(status_code=status.HTTP_200_OK, content=data)
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


# create new user
@app.post("/users/create")
def create_user(user_data: User):
    data = load_data()

    if user_data.id in data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="enter valid id this might be wrong !!",
        )
    data[user_data.id] = user_data.model_dump(exclude=["id"])
    save_data(data=data)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=f"user {user_data.name} created successfully",
    )


# get user by id
@app.get("/users/{id}")
def get_user(id: str):
    data = load_data()
    if id not in data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid user id enter a valid id!!",
        )

    user_data = data[id]
    return JSONResponse(status_code=status.HTTP_200_OK, content=user_data)


@app.put("/users/{id}/update")
def update_user(
    user_data: User_update,
    id: str = Path(title="enter user is exp: u001 ,u010", min_length=4, max_length=7),
):
    data = load_data()
    if id not in data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid user id enter a valid id",
        )

    updated_dict = user_data.model_dump(exclude_unset=True)
    user_info = data[id]
    for k, v in updated_dict.items():
        user_info[k] = v

    data[id] = user_info
    save_data(data=data)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content=f"user: {id} updated successfully!!"
    )


@app.delete("/users/{id}/delete")
def delete_user(id: str):
    data = load_data()
    if id not in data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid user id enter a valid id",
        )
    del data[id]
    save_data(data=data)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content=f"user: {id} deleted successfully!!"
    )
