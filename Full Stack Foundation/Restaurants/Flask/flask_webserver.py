from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurant.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def restaurantList():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)

@app.route('/add/restaurant/',  methods=['GET', 'POST'])
def newRestaurant():
    return "Dummy"


@app.route('/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantDetail(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    output = restaurant.name
    return output


@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    """
    page to create a new menu item.
    """
    return "page to create a new menu item."


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
    return "page to edit a menu item. "


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item."


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
