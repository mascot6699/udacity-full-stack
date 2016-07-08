"""
Contains all enities used for the project
"""

from google.appengine.ext import db


class Art(db.Model):
    """
    ASCII art entity.
    """
    title = db.StringProperty(required=True)
    art = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)


class Post(db.Model):
    """
    Blog post entity.
    """
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created_at = db.DateTimeProperty(auto_now_add=True)
    modified_at = db.DateTimeProperty(auto_now=True)