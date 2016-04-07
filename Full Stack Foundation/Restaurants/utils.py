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


def create_restaurant(name):
    """

    :return:
    """
    new_restaurant = Restaurant(name=name)
    session.add(new_restaurant)
    session.commit()


def get_restaurant_by_id(id):
    """
    :return:
    """
    restaurant = session.query(Restaurant).filter_by(id=id).one()
    return restaurant


def rename_restaurant(id, name):
    """

    :return:
    """
    restaurant = session.query(Restaurant).filter_by(id=id).one()
    if restaurant != []:
        restaurant.name = name
        session.add(restaurant)
        session.commit()