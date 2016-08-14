from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
db_session = DBSession()


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
    app.debug = True
    app.run(host='0.0.0.0', port=8080)