from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, make_response, session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from oauth2client import client, crypt

from database_setup import Base, Restaurant, MenuItem, User

import random, string, requests, json


app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenuwithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

WEB_CLIENT_ID = json.loads(open('client_secret.json', 'r').read())['web']['client_id']


def create_user(login_session):
    newUser = User(name=login_session['username'], 
        email=login_session['email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def get_user_info(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def get_user_id(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# For disconnecting from google plus
@app.route('/gdisconnect')
def gdisconnect():

    if login_session['email'] is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['state']
        del login_session['auth_type']

        flash("Goodbye!")
        return redirect('/')


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

    code = request.data

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
    stored_gplus_id = login_session.get('gplus_id')

    if gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # see if user exists, if it doesn't make a new one
    user_id = get_user_id(idinfo["email"])
    if not user_id:
        user_id = create_user(login_session)

    # set session variables    
    login_session['user_id'] = user_id
    login_session['auth_type'] = 'gplus'
    login_session['username'] = idinfo['name']
    login_session['picture'] = idinfo['picture']
    login_session['email'] = idinfo['email']

    # response to be shown
    output = '<h3>Welcome, {}!</h3><img src="{}" class="google-img">'.format(login_session['username'], login_session['picture'])
    flash("You are now logged in as {}".format(login_session['username']))
    return output



@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secret.json', 'r').read())['web']['app_id']
    app_secret = json.loads(open('fb_client_secret.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id={}&client_secret={}&fb_exchange_token={}'.format(app_id, app_secret, access_token)
    result = requests.get(url)
    token = result.text.split("&")[0]

    url = 'https://graph.facebook.com/v2.7/me?{}&fields=name,id,email'.format(token)
    data = requests.get(url).json()
    # The token must be stored in the login_session in order to properly logout, let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token
    login_session['auth_type'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    data = requests.get(url).json()

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = get_user_id(login_session['email'])
    if not user_id:
        user_id = create_user(login_session)
    login_session['user_id'] = user_id

    # response to be shown
    output = '<h3>Welcome, {}!</h3><img src="{}" class="google-img">'.format(login_session['username'], login_session['picture'])
    flash("You are now logged in as {}".format(login_session['username']))
    return output


@app.route('/logout')
def logout():
    if login_session['auth_type'] == 'gplus':
        return redirect(url_for('gdisconnect'))


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
