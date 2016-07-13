"""
This file will contain all the entities required for Blog app
"""
from google.appengine.ext import db

class User(db.Model):
    """
    Entity to store for User.
    """
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)  # hash of password will be stored
    email = db.StringProperty()
    fullname = db.StringProperty()
    about = db.StringProperty()