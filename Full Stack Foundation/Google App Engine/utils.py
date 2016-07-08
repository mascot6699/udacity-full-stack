import re
from string import letters

USER_REGEX = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_REGEX = re.compile(r"^.{3,20}$")
EMAIL_REGEX  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
SECRET = 'umang'

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

def make_secure_key(key):
    """
    Generates a key to be saved in cookie after hashing it with a secret salt
    """
    return '%s|%s' % (key, hmac.new(SECRET, key).hexdigest())

def check_secure_key(secure_key):
    """
    Checks a key by if first value matches the second value of key
    :returns: None if it does not match
    """
    key = secure_key.split('|')[0]
    if secure_val == make_secure_val(val):
        return val