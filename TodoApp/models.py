from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, index=True) 
    email = Column(String, unique=True)
    username = Column(String,unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean ,default=True)
    role = Column(String)
    phone_number = Column(Integer, nullable=True)
    phone_number2 = Column(Integer, nullable=True)


class Todos(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key = True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    extra_explan = Column(String, nullable=True)
    extra_explan2 = Column(String, nullable=True)


