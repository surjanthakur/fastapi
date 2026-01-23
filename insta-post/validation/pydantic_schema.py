from datetime import date
from pydantic import BaseModel, EmailStr
from typing import List


# user table validation
class user_schema(BaseModel):
    username: str
    email: EmailStr


# post table validation
class post_schema(BaseModel):
    title: str
    content: str
    created_at: date


# profile table validation
class profile_schema(BaseModel):
    created_at: date
    bio: str
    posts: List[post_schema]

# combined user profile schema
class user_profile_schema(BaseModel):
    username: str
    email: EmailStr
    profiles: List[profile_schema]

# request profile schema
class request_profile(BaseModel):
    bio:str