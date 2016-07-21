"""
Contains CRUD views of comments
"""
from google.appengine.ext import db

from entities.entity import Post, User, Comment
from handlers.auth import AuthHandler

from datetime import datetime
import copy


class AddComment(AuthHandler):

    def post(self, post_id):
        """
        Create a new comment for the post with post_id as in params
        """
        if not self.user:
            error = "You must be logged in to comment"
            self.render('login.html', error=error)
        else:
            post = Post.get_by_id(int(post_id))
            user_obj = User.get_by_id(int(self.user))
            comment = self.request.get('comment')
            comment = Comment(comment=comment, user=user_obj, post=post)
            comment.put()
            self.redirect("/blog/{}".format(post.slug))
