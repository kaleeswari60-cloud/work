from pydantic import BaseModel
from datetime import date
from typing import List


# ---------------- HOBBIES ----------------

class HobbyCreate(BaseModel):
    hobby_name: str


class Hobby(BaseModel):
    id: int
    hobby_name: str

    class Config:
        from_attributes = True


# ---------------- USERS ----------------

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    email: str
    password: str
    country: str
    city: str
    hobbies: List[int]


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    country: str
    city: str
    hobbies: List[Hobby]

    class Config:
        from_attributes = True