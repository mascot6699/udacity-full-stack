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

    @property
    def serialize(self):
        """
        Return object data in serialized format
        """
        return {
            'id': self.id,
            'name': self.name,
            'website': self.website,
            }


class MenuItem(Base):
    __tablename__ = 'menu_item'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    @property
    def serialize(self):
        """
        Return object data in serialized format
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price
            }


engine = create_engine('sqlite:///restaurant.db')
Base.metadata.create_all(engine)