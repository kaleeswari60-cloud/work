from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(Date)
    email = Column(String, unique=True)
    password = Column(String)
    country = Column(String)
    city = Column(String)

    hobbies = relationship("UserHobby", back_populates="user")


class Hobby(Base):
    __tablename__ = "hobbies"

    id = Column(Integer, primary_key=True)
    hobby_name = Column(String, unique=True)

    users = relationship("UserHobby", back_populates="hobby")


class UserHobby(Base):
    __tablename__ = "user_hobbies"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    hobby_id = Column(Integer, ForeignKey("hobbies.id"))

    user = relationship("User", back_populates="hobbies")
    hobby = relationship("Hobby", back_populates="users")