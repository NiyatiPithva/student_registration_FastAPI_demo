from sqlalchemy import Column,Integer,String
from database import engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Student(Base):
    __tablename__ = "studnets"

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String(50))
    email = Column(String(50))
    course = Column(String(50))

# auto creation in mysql
Base.metadata.create_all(bind = engine)