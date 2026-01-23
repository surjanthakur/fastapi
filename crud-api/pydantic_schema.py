from pydantic import BaseModel, EmailStr, Field, computed_field
from typing import List, Optional, Literal


class Patient(BaseModel):
    id: str
    name: str
    email: EmailStr
    weight: float
    age: int
    gender: Literal["male", "female", "other"]
    blood_group: str
    disease: Optional[List[str]] = None
    admitted: bool


@computed_field
@property
def bmi(self) -> float:
    bmi = round(self.weight / (self.height**2), 2)
    return bmi


class Patient_update(BaseModel):
    name: Optional[str] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)
    weight: Optional[float] = Field(default=None)
    age: Optional[int] = Field(default=None)
    disease: Optional[List[str]] = None
    admitted: Optional[bool] = Field(default=None)


class Tweety(BaseModel):
    id: str
    username: str = Field(..., min_length=5, max_length=60)
    content: str = Field(..., min_length=10, max_length=300)


class Tweety_update(BaseModel):
    content: str = Field(..., min_length=10, max_length=300)
