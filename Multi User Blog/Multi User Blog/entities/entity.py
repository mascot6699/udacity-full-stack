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


class Post(db.Model):
    """
    Entity to store a Blog Post.
    """
    title = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    user = db.ReferenceProperty(User, required=True, collection_name='posts')
    is_draft = db.BooleanProperty(default=False)
    modified_at = db.DateTimeProperty(auto_now=True)
    created_at = db.DateTimeProperty(auto_now_add=True)
    published_at = db.DateTimeProperty(required=True)


class Like(db.Model):
    """
    Store the like of a Blog Post
    """
    user = db.ReferenceProperty(User, required=True, collection_name='likes')
    post = db.ReferenceProperty(Post, required=True, collection_name='likes')


class Comment(db.Model):
    """
    Store the comment of a Blog Post.
    """
    post = db.ReferenceProperty(Post, required=True, collection_name='comments')
    user = db.ReferenceProperty(User, required=True, collection_name='comments')
    comment = db.StringProperty(required=True)
    created_at = db.DateTimeProperty(auto_now_add=True)