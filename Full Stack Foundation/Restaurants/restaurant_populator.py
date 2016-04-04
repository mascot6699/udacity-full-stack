from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base

engine = create_engine('sqlite:///restaurant.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()

restaurant_names = ["Urban Burger", "Super Stir Fry", "Panda Garden", "Thyme for That Vegetarian Cuisine",
                    "Tony\'s Bistro", "Auntie Ann\'s Diner", "Cocina Y Amor"]
for i in restaurant_names:

    restaurant = Restaurant(name=i)
    session.add(restaurant)
    session.commit()
