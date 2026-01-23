from datetime import date
from sqlmodel import Relationship, SQLModel, Field, true
from pydantic import field_validator, AfterValidator
import uuid
from typing import Annotated, List


# User table ------------------------->
class User(SQLModel, table=True):
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), unique=True, primary_key=True
    )
    username: Annotated[
        str,
        Field(..., min_length=3, max_length=20),
        AfterValidator(lambda v: v.title()),
    ]
    email: str = (Field(..., unique=True),)
    created_at: date = Field(default_factory=date.today)

    @field_validator("email")
    @classmethod
    def email_validator(clas, val):
        valid_part = val.split("@")[-1]
        if valid_part not in ["gmail.com"]:
            raise ValueError("invalid email it should be [gmail.com]")
        return val


# Profile table --------------------------->
class Profile(SQLModel, table=True):
    created_at: date = Field(default_factory=date.today)
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), unique=True, primary_key=True
    )
    user_id: str = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")
    bio: Annotated[
        str, Field(min_length=10, max_items=40), AfterValidator(lambda v: v.title())
    ]
    posts: List["Post"] = Relationship(back_populates="profile")


# Post table ----------------------------------->
class Post(SQLModel, table=true):
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), unique=True, primary_key=True
    )
    title: Annotated[
        str, Field(min_length=5, max_items=40), AfterValidator(lambda v: v.title())
    ]
    content: Annotated[
        str, Field(min_length=10, max_items=200), AfterValidator(lambda v: v.title())
    ]
    profile_id: str = Field(
        foreign_key="profile.id", nullable=False, ondelete="CASCADE"
    )
    profile: "Profile" = Relationship(back_populates="posts")
    created_at: date = Field(default_factory=date.today)
