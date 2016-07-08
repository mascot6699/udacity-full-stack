from .base import Handler
import utils


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