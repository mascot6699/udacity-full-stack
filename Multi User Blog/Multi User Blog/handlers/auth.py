from .base import Handler
from entities.entity import User
import utils


class AuthHandler(Handler):
    """
    Adds common utility methods needed for authentication
    """

    def set_secure_cookie(self, name, key):
        """
        Store a cookie after hashing
        """
        cookie_val = utils.make_secure_key(key)
        self.response.headers.add_header(
            'Set-Cookie','%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        """
        Read a cookie and return if valid"
        """
        cookie_val = self.request.cookies.get(name)
        return cookie_val and utils.check_secure_key(cookie_val)

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
        if uid and User.get_by_id(int(uid)):
            self.user = uid
            self.blog_user = User.get_by_id(int(uid))
        else:
            self.user = None
            self.blog_user = None

    def render(self, template, **kw):
        kw['blog_user'] = self.blog_user
        self.write(self.render_str(template, **kw))


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
            self.redirect('/mock/signup/')


class Signup(AuthHandler):

    def get(self):
        """
        Render signup page
        """
        if not self.user:
            self.render("register.html")
        else:
            self.redirect('/')

    def post(self):
        """
        Redirect to welcome page if form is valid else shows form 
        with error details
        """
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')
        params = dict(username=self.username, email=self.email)

        if not utils.valid_username(self.username):
            params['error_username'] = "That's not a valid username."
            have_error = True
        if not utils.valid_password(self.password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif self.password != self.verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True
        if not utils.valid_email(self.email):
            params['error_email'] = "That's not a valid email."
            have_error = True
        if have_error:
            self.render('register.html', **params)
        else:
            self.done()

    def done(self, *a, **kw):
        raise NotImplementedError


class Register(Signup):
    """
    Registers the user instance so that user can log back again
    """
    def done(self):
        """
        Saves an user instance if possible and redirects to login page
        """
        u = User.by_name(self.username)
        if u:
            msg = 'That user already exists.'
            self.render('register.html', error_username=msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()
            self.login(u)
            self.redirect('/')


class LogoutHandler(AuthHandler):
    """
    Logs out the user
    """
    def get(self):
        self.logout()
        logged_out = True
        self.render('login.html', logged_out=logged_out)


class LoginHandler(AuthHandler):
    """
    Logs in user
    """
    def get(self):
        """
        Shows login form if not logged in
        """
        if not self.user:
            self.render('login.html')
        else:
            self.redirect('/')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/')
        else:
            msg = 'Invalid login'
            self.render('login.html', error=msg)