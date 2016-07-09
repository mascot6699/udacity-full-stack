"""
Contains all enities used for the project
"""

from google.appengine.ext import db
import utils

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


class User(db.Model):
    """
    User entity
    Saves hashed password instead of password directly
    """
    username = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()

    @classmethod
    def by_name(cls, username):
        """
        Finds a user by username
        """
        user = User.all().filter('username =', username).get()
        return user

    @classmethod
    def register(cls, username, pw, email=None):
        """
        Converts password to hashed password and initiates an instance
        """
        pw_hash = utils.make_pw_hash(username, pw)
        return User(username=username, pw_hash=pw_hash, email=email)

    @classmethod
    def login(cls, username, pw):
        """
        Returns a user instance if user and password match
        """
        u = cls.by_name(username)
        if u and utils.valid_pw(username, pw, u.pw_hash):
            return u