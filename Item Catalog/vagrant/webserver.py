from flask import Flask, session, url_for, flash, jsonify, redirect, render_template, make_response, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item, User

from oauth2client import client, crypt
from functools import wraps
import random
import string
import json

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
db_session = DBSession()

WEB_CLIENT_ID = json.loads(open('client_secret.json', 'r').read())[
    'web']['client_id']


def create_user(session):
    newUser = User(
        name=session['username'],
        email=session['email'],
        picture=session['picture'])
    db_session.add(newUser)
    db_session.commit()
    user = db_session.query(User).filter_by(email=session['email']).one()
    return user.id


def get_user_info(user_id):
    user = db_session.query(User).filter_by(id=user_id).one()
    return user


def get_user_id(email):
    try:
        user = db_session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def login_required(f):
    @wraps(f)
    def df(*args, **kwargs):
        if not session or session.get('user_id', None) is None:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return df


# For disconnecting from google plus
@app.route('/gdisconnect')
def gdisconnect():

    if session['email'] is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        del session['username']
        del session['email']
        del session['picture']
        del session['state']
        del session['auth_type']
        del session['user_id']

        flash("Goodbye!")
        return redirect('/')


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    code = request.data

    try:
        idinfo = client.verify_id_token(code, WEB_CLIENT_ID)
        # If multiple clients access the backend server:
        if idinfo['aud'] not in [WEB_CLIENT_ID]:
            raise crypt.AppIdentityError("Unrecognized client.")
        if idinfo['iss'] not in ['accounts.google.com',
                                 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")
    except crypt.AppIdentityError as e:
        response = make_response(json.dumps(e.message), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    gplus_id = idinfo['sub']
    stored_gplus_id = session.get('gplus_id')

    if gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # set session variables

    session['auth_type'] = 'gplus'
    session['username'] = idinfo['name']
    session['picture'] = idinfo['picture']
    session['email'] = idinfo['email']

    # see if user exists, if it doesn't make a new one
    user_id = get_user_id(idinfo["email"])
    print user_id
    if not user_id:
        user_id = create_user(session)

    session['user_id'] = user_id

    # response to be shown
    output = '<h3>Welcome, {}!</h3><img src="{}" class="google-img">'.format(
        session['username'], session['picture'])
    flash("You are now logged in as {}".format(session['username']))
    return output


@app.route('/logout')
def logout():
    """
    Call the corresponding logout function by checking auth_type
    """
    if session['auth_type']:
        if session['auth_type'] == 'gplus':
            return redirect(url_for('gdisconnect'))
    return redirect(url_for('login'))


# Create anti-forgery state token
@app.route('/login')
def login():
    state = ''.join(
        random.choice(
            string.ascii_uppercase +
            string.digits) for x in xrange(32))
    session['state'] = state
    return render_template("login.html", state=state)


@app.route('/')
def categoryList():
    """
    List down all the categories available on our site
    """
    categories = db_session.query(Category).all()
    return render_template('categories.html', categories=categories)


@app.route('/add/category/', methods=['GET', 'POST'])
@login_required
def newCategory():
    """
    Show addition of category form
    """
    # if session and session.get('user_id', None) is None:
    if request.method == 'POST':
        newCategory = Category(
            name=request.form['name'],
            user_id=session['user_id'])
        db_session.add(newCategory)
        db_session.commit()
        flash("New category created!")
        return redirect(url_for('categoryList'))
    else:
        return render_template('add_category.html')
    # return redirect(url_for('login'))


@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
@login_required
def deleteCategory(category_id):
    """
    Page to delete a category.
    """
    error = False
    category = db_session.query(Category).filter_by(id=category_id).one()
    if category.user_id == session['user_id']:
        if request.method == 'POST':
            db_session.delete(category)
            db_session.commit()
            flash("Category has been deleted!")
            return redirect(url_for('categoryList'))
        else:
            if category.user_id != session['user_id']:
                error = True
                flash("Only owner can delete their category!")
            return render_template(
                'delete_category.html', category=category, error=error)
    else:
        flash("Only owner can delete their category!")
        return redirect(url_for('categoryList'))


@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
@login_required
def editCategory(category_id):
    """
    Page to edit a category.
    """
    error = False
    category = db_session.query(Category).filter_by(id=category_id).one()
    if category.user_id == session['user_id']:
        if request.method == 'POST':
            category.name = request.form['name'] if request.form[
                'name'] else category.name
            db_session.add(category)
            db_session.commit()
            flash("Category has been edited!")
            return redirect(url_for('categoryList'))
        else:
            if category.user_id != session['user_id']:
                error = True
                flash("Only owner can edit their category!")
            return render_template('edit_category.html',
                                   category=category, error=error)
    else:
        flash("Only owner can delete their category!")
        return redirect(url_for('categoryList'))


@app.route('/<int:category_id>/')
@app.route('/categories/<int:category_id>/')
def categoryDetail(category_id):
    category = db_session.query(Category).filter_by(id=category_id).one()
    items = db_session.query(Item).filter_by(category_id=category_id)
    return render_template('items.html', category=category, items=items)


@app.route('/category/<int:category_id>/new/', methods=['GET', 'POST'])
@login_required
def newItem(category_id):
    """
    page to create a new  item.
    """
    if request.method == 'POST':
        newItem = Item(name=request.form['name'], description=request.form['description'],
                       price=request.form['price'], category_id=category_id, 
                       user_id=session['user_id'])
        db_session.add(newItem)
        db_session.commit()
        flash("Item has been created!")
        return redirect(url_for('categoryDetail', category_id=category_id))
    else:
        return render_template('add_item.html', category_id=category_id)


@app.route('/category/<int:category_id>/<int:id>/edit/',
           methods=['GET', 'POST'])
@login_required
def editItem(category_id, id):
    """
    page to edit a item.
    """
    error = False
    editedItem = db_session.query(Item).filter_by(id=id).one()
    if editedItem.user_id == session['user_id']:
        if request.method == 'POST':
            editedItem.name = request.form['name'] if request.form[
                'name'] else editedItem.name
            if request.form['description']:
                editedItem.description = request.form['description']
            if request.form['price']:
                editedItem.price = request.form['price']
            db_session.add(editedItem)
            db_session.commit()
            flash("Item has been edited!")
            return redirect(url_for('categoryDetail', category_id=category_id))
        else:
            if editedItem.user_id != session['user_id']:
                error = True
                flash("Only owner can edit their items!")
            return render_template(
                'edit_item.html', item=editedItem, category_id=category_id, error=error)
    else:
        flash("Only owner can edit their items!")
        return redirect(url_for('categoryDetail'))


@app.route('/category/<int:category_id>/<int:id>/delete/',
           methods=['GET', 'POST'])
@login_required
def deleteItem(category_id, id):
    """
    page to delete a item.
    """
    error = False
    item = db_session.query(Item).filter_by(id=id).one()
    if item.user_id == session['user_id']:
        if request.method == 'POST':
            db_session.delete(item)
            db_session.commit()
            flash("Item has been deleted!")
            return redirect(url_for('categoryDetail', category_id=category_id))
        else:
            if item.user_id != session['user_id']:
                error = True
                flash("Only owner can delete their items!")
            return render_template(
                'delete_item_confirm.html', item=item, error=error)
    else:
        flash("Only owner can delete their items!")
        return redirect(url_for('categoryDetail'))


# APIS for the catalog app
@app.route('/all/JSON')
def categories_api():
    categories = db_session.query(Category).all()
    return jsonify(categories=[category.serialize for category in categories])


@app.route('/<int:category>/JSON')
def items_api(category):
    items = db_session.query(Item).filter_by(category_id=category).all()
    return jsonify(items=[item.serialize for item in items])


@app.route('/<int:category>/item/<int:item_id>/JSON')
def item_api(category, item_id):
    item = db_session.query(Item).filter_by(id=item_id).one()
    return jsonify(item.serialize)


if __name__ == '__main__':
    # app.debug = True
    app.secret_key = "not_very_secretive"
    app.run(host='0.0.0.0', port=8080)
