"""
Defines the database setup to make tables in db
"""
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Shelter(Base):
    """
    Schema for shelter database
    """
    __tablename__ = "shelter"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    address = Column(String(500))
    city = Column(String(100))
    state = Column(String(100))
    zipCode = Column(String(9))
    website = Column(String(100))



engine = create_engine('sqlite:///puppy.db')
Base.metadata.create_all(engine)