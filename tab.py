from sqlalchemy import Column, Integer, String
from depend import Base

class Employee(Base):
    __tablename__ = "simple_user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    address = Column(String)
