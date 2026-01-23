from pydantic import EmailStr, field_validator
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel
from typing import List, Optional
import uuid


class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str = Field(min_length=3, max_length=20)
    email: EmailStr = Field(unique=True)
    tweets: List["Tweet"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Tweet(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    content: str = Field(min_length=10, max_length=400)
    user_id: str = Field(..., nullable=False, foreign_key="user.id", ondelete="CASCADE")
    user: Optional["User"] = Relationship(back_populates="tweets")

    @field_validator("content", mode="after")
    @classmethod
    def tansform_content(cls, value):
        return value.title()
