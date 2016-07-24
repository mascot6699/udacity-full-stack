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
import webapp2
from handlers.index import IndexHandler
from handlers.auth import Register, LoginHandler, LogoutHandler
from handlers.blog import AddBlog, EditBlog, Permalink, BlogList, DeleteBlog
from handlers.comment import AddComment, DeleteComment, CommentError, UpdateComment
from handlers.likes import LikeBlog, LikeError


app = webapp2.WSGIApplication([
    ('/', BlogList),
    ('/allposts', BlogList),
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/register', Register),
    ('/blog/add', AddBlog),
    ('/blog/edit/([0-9]+)', EditBlog),
    ('/blog/like/([0-9]+)', LikeBlog),
    ('/blog/delete/([0-9]+)', DeleteBlog),
    ('/blog/([a-z0-9\-]+)', Permalink),
    ('/blog/([0-9]+)/add/comment', AddComment),
    ('/delete/comment/([0-9]+)', DeleteComment),
    ('/edit/comment/([0-9]+)', UpdateComment),
    ('/comment/error', CommentError),
    ('/like/error', LikeError),
], debug=True)
