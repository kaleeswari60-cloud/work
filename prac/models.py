from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

# Association Table (Many-to-Many)
user_hobbies = Table(
    "user_hobbies",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("hobby_id", Integer, ForeignKey("hobbies.id"))
)


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

    hobbies = relationship(
        "Hobby",
        secondary=user_hobbies,
        back_populates="users"
    )


class Hobby(Base):
    __tablename__ = "hobbies"

    id = Column(Integer, primary_key=True)
    hobby_name = Column(String, unique=True)

    users = relationship(
        "User",
        secondary=user_hobbies,
        back_populates="hobbies"
    )