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


# ---------------- USER-HOBBY RELATION ----------------

class UserHobby(BaseModel):
    hobby: Hobby

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
    hobbies: List[int]   # list of hobby IDs selected by user


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    country: str
    city: str
    hobbies: List[UserHobby]   # display hobbies with user

    class Config:
        from_attributes = True