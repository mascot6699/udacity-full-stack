"""
This file will contain all the entities required for Blog app
"""
from google.appengine.ext import db

import utils, fields


class User(db.Model):
    """
    Entity to store for User.
    """
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)  # hash of password will be stored
    email = db.StringProperty()
    fullname = db.StringProperty()
    about = db.StringProperty()

    @classmethod
    def by_name(cls, username):
        """
        Finds a user by username
        """
        user = User.all().filter('username =', username).get()
        return user

    @classmethod
    def register(cls, username, password, email=None):
        """
        Converts password to hashed password and initiates an instance
        """
        pw_hash = utils.make_pw_hash(username, password)
        return User(username=username, password=pw_hash, email=email)

    @classmethod
    def login(cls, username, password):
        """
        Returns a user instance if user and password match
        """
        user = cls.by_name(username)
        if user and utils.valid_pw(username, password, user.password):
            return user


class Post(db.Model):
    """
    Entity to store a Blog Post.
    """
    title = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    slug = fields.SlugProperty(title)
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
    comment = db.TextProperty(required=True)
    created_at = db.DateTimeProperty(auto_now_add=True)