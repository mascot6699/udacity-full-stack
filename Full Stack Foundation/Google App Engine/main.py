#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os

import webapp2
import jinja2

import utils

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True) # Don't forget to autoescape


class Handler(webapp2.RequestHandler):
    """
    Jinja request handler base class
    """
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class ShoppingListHandler(Handler):
    """
    Shopping list handler
    """
    def get(self):
        """
        Shows form back.
        """
        items = self.request.get_all("food")
        self.render("shopping_list.html", items=items)


class Rot13Handler(Handler):
    """
    Rotation by 13 ceaser cipher implemented
    """

    def get(self):
        self.render('rot13-form.html')

    def post(self):
        rot13 = ''
        text = self.request.get('text')
        if text:
            rot13 = text.encode('rot13')

        self.render('rot13-form.html', text = rot13)


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


class IndexPageHandler(Handler):
    """
    """
    def get(self):
        """
        Landing or Index page handler
        """
        self.render('index.html')


app = webapp2.WSGIApplication(
    [('/', IndexPageHandler),
     ('/shopping/list/', ShoppingListHandler),
     ('/rot13/', Rot13Handler),
     ('/welcome/', WelcomePage),
     ('/signup/', Signup),
    ], debug=True)
