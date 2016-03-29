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
    Schema for shelter table
    """
    __tablename__ = "shelter"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    address = Column(String(500))
    city = Column(String(100))
    state = Column(String(100))
    zipCode = Column(String(9))
    website = Column(String(100))


class Puppy(Base):
    """
    Schema for puppy table
    """
    __tablename__ = "puppy"

    name = Column(String(100), nullable=False)
    dob = Column(Date)
    gender = Column(String(6))
    weight = Column(Numeric)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)

engine = create_engine('sqlite:///puppy.db')
Base.metadata.create_all(engine)