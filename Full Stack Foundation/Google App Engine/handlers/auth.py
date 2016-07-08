from .base import Handler
import utils

class AuthHandler(Handler):
    """
    Adds common utility methods needed for authentication
    """

    def set_secure_cookie(self, name, val):
        """
        Store a cookie after hashing
        """
        cookie_val = utils.make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie','%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        """
        Read a cookie and return if valid"
        """
        cookie_val = self.request.cookies.get(name)
        return cookie_val and utils.check_secure_val(cookie_val)

    def login(self, user):
        """
        Adds the user_id cookie to login user
        """
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        """
        Removes the user_id cookie value to logout user
        """
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        """
        Auth middleware to set self.user if set in cookie
        """
        Handler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        if User.get_by_id(uid(int(uid)):
            self.user = uid 


class WelcomePage(Handler):
    """
    """
    def get(self):
        """
        Welcome a valid user or redirect to signup page
        """
        username = self.request.get('username')
        if utils.valid_username(username):
            self.render('welcome.html', username=username)
        else:
            self.redirect('/signup/')


class Signup(Handler):

    def get(self):
        """
        Render signup page
        """
        self.render("signup-form.html")

    def post(self):
        """
        Redirect to welcome page if form is valid else shows form 
        with error details
        """
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        params = dict(username=username, email=email)

        if not utils.valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True
        if not utils.valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True
        if not utils.valid_email(email):
            params['error_email'] = "That's not a valid email."
            have_error = True
        if have_error:
            self.render('signup-form.html', **params)
        else:
            self.redirect('/welcome/?username=' + username)