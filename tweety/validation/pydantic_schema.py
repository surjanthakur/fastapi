from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import List


# Request schema for user registration/creation
# Validates incoming user data and ensures email is from valid domain (gmail.com only)
# Also auto-capitalizes the user's name
class pydantic_user(BaseModel):
    name: str = Field(min_length=3, max_length=20)
    email: EmailStr = Field(unique=True)

    @field_validator("email", mode="after")
    @classmethod
    def email_validator(cls, value):
        valid_domains = ["gmail.com"]
        domain_name = value.split("@")[-1]
        if domain_name not in valid_domains:
            raise ValueError("opps! not a valid gmail.")
        return value

    @field_validator("name", mode="after")
    @classmethod
    def name_validator(cls, value):
        return value.capitalize()


# Request schema for tweet creation
# Validates tweet content length (10-600 characters) and auto-formats to title case
class pydantic_tweet(BaseModel):
    content: str = Field(min_length=10, max_length=600)

    @field_validator("content", mode="after")
    @classmethod
    def transform_content(cls, value):
        return value.title()


# Response schema for returning tweets with associated user information
# Used when fetching tweets to include both tweet content and user details
class response_tweets(BaseModel):
    content: str = Field(min_length=10, max_length=600)
    user: pydantic_user


# Response schema for returning users with associated tweets information
# Used when fetching users to include both tweets content and user details.
class response_user(BaseModel):
    created_at: datetime
    name: str = Field(min_length=3, max_length=20)
    email: EmailStr = Field(unique=True)
    tweets: List[pydantic_tweet]
