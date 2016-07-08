#!/usr/bin/env python

import webapp2

from handlers.ascii import AsciiForumHandler
from handlers.auth import WelcomePage, Signup
from handlers.blogs import BlogListHandler, NewBlogHandler, Permalink
from handlers.index import IndexPageHandler
from handlers.rot13 import Rot13Handler
from handlers.shopping import ShoppingListHandler


app = webapp2.WSGIApplication([
    ('/', IndexPageHandler),
    ('/ascii/', AsciiForumHandler),
    ('/blog/', BlogListHandler),
    ('/blog/([0-9]+)/', Permalink),
    ('/blog/add/', NewBlogHandler),
    ('/rot13/', Rot13Handler),
    ('/signup/', Signup),
    ('/shopping/list/', ShoppingListHandler),
    ('/welcome/', WelcomePage)], debug=True)
