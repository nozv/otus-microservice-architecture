from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from src.db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(256))
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String)
    phone = Column(String)
