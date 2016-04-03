"""
Defines the database setup to make tables in db
"""
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()


class Restaurant(Base):
    """
    Schema for restaurant table
    """
    __tablename__ = "restaurant"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    website = Column(String(100), nullable=True)


engine = create_engine('sqlite:///restaurant.db')
Base.metadata.create_all(engine)