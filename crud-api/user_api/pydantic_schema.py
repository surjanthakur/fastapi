from pydantic import BaseModel, EmailStr, Field
from typing import Annotated


class User(BaseModel):
    id: Annotated[
        str,
        Field(
            min_length=4, max_length=7, description="enter user id exp: u0010 , u003"
        ),
    ]
    name: str = Field(min_length=3, max_length=20)
    age: int = Field(gt=18)
    city: str = Field(min_length=3, max_length=20)
    work_role: str = Field(min_length=3, max_length=20)
    email: EmailStr


class User_update(BaseModel):
    name: str = Field(min_length=3, max_length=20)
    age: int = Field(gt=18)
    city: str = Field(min_length=3, max_length=20)
    work_role: str = Field(min_length=3, max_length=20)
    email: EmailStr
