from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, make_response, session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from oauth2client import client, crypt

from database_setup import Base, Restaurant, MenuItem

import random, string, requests, json


app = Flask(__name__)

engine = create_engine('sqlite:///restaurant.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

WEB_CLIENT_ID = json.loads(open('client_secret.json', 'r').read())['web']['client_id']


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template("login.html", state=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    # url = 'https://www.googleapis.com/oauth2/v3/tokeninfo'
    # params = {'id_token': code}
    # result = requests.get(url, params=params)

    try:
        idinfo = client.verify_id_token(code, WEB_CLIENT_ID)
        # If multiple clients access the backend server:
        if idinfo['aud'] not in [WEB_CLIENT_ID]:
            raise crypt.AppIdentityError("Unrecognized client.")
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")
    except crypt.AppIdentityError as e:
        response = make_response(json.dumps(e.message), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    gplus_id = idinfo['sub']

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')

    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    login_session['username'] = idinfo['name']
    login_session['picture'] = idinfo['picture']
    login_session['email'] = idinfo['email']

    output = '<h3>Welcome, {}!</h3><img src="{}" class="google-img">'.format(login_session['username'], login_session['picture'])
    flash("you are now logged in as {}".format(login_session['username']))
    return output


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


@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    """
    Page to delete a restaurant.
    """
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        flash("Restaurant has been deleted!")
        return redirect(url_for('restaurantList'))
    else:
        return render_template('delete_restaurant.html', restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    """
    Page to edit a restaurant. 
    """
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        restaurant.name = request.form['name'] if request.form['name'] else restaurant.name
        restaurant.website = request.form['website'] if request.form['description'] else restaurant.website
        session.add(restaurant)
        session.commit()
        flash("Restaurant has been edited!")
        return redirect(url_for('restaurantList'))
    else:
        return render_template('edit_restaurant.html', restaurant=restaurant)


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
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form['description'], 
            price=request.form['price'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("Menu has been created!")
        return redirect(url_for('restaurantDetail', restaurant_id=restaurant_id))
    else:
        return render_template('add_menu_item.html', restaurant_id=restaurant_id)


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


@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(menu=[i.serialize for i in items])


@app.route('/restaurants/JSON/')
def restaurantJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(restaurants=[i.serialize for i in restaurants])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def menuItemJSON(restaurant_id, menu_id):
    """
    """
    # TODO: check if menu belongs to restaurant?
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(menu=menuItem.serialize)


if __name__ == '__main__':
    app.debug = True
    app.secret_key = "not_very_secretive"
    app.run(host='0.0.0.0', port=8080)
