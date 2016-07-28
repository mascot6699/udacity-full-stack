from flask import Flask, render_template, request, flash, redirect, url_for
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
    """
    List down all the restaurants available on our site
    """
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/add/restaurant/', methods=['GET', 'POST'])
def newRestaurant():
    """
    Show addition of restaurant form
    """
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'], website=request.form['website'])
        session.add(newRestaurant)
        session.commit()
        flash("New restaurant created!")
        return redirect(url_for('restaurantList'))
    else:
        return render_template('add_restaurant.html')


@app.route('/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantDetail(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    return render_template('menu.html', restaurant=restaurant, items=items)


@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    """
    page to create a new menu item.
    """
    return "page to create a new menu item."


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    """
    page to edit a menu item. 
    """
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        editedItem.name = request.form['name'] if request.form['name'] else editedItem.name
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        session.add(editedItem)
        session.commit()
        flash("Menu has been edited!")
        return redirect(url_for('restaurantDetail', restaurant_id=restaurant_id))
    else:
        return render_template('edit_menu_item.html', item=editedItem, restaurant_id=restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    """
    page to delete a menu item.
    """
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash("Menu has been deleted!")
        return redirect(url_for('restaurantDetail', restaurant_id=restaurant_id))
    else:
        return render_template('delete_item_confirm.html', item=item)


if __name__ == '__main__':
    app.debug = True
    app.secret_key = "not_very_secretive"
    app.run(host='0.0.0.0', port=5000)
