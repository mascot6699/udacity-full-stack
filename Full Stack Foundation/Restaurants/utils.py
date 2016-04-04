from database_setup import Base, Restaurant
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///restaurant.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def get_restaurants():
    """
    :return: a list of restaurants objects
    """
    return session.query(Restaurant).all()