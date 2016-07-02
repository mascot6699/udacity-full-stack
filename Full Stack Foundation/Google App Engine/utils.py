import re
from string import letters

USER_REGEX = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_REGEX = re.compile(r"^.{3,20}$")
EMAIL_REGEX  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')

def valid_username(username):
    """
    Determines is an username is valid or not
    """
    return username and USER_REGEX.match(username)

def valid_password(password):
    """
    Determines if a password is valid or not
    """
    return password and PASS_REGEX.match(password)

def valid_email(email):
    """
    Determines if an email is valid or not
    """
    return not email or EMAIL_REGEX.match(email)