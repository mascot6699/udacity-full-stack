"""
Handles likes post request and also error handlings of those cases
"""
from google.appengine.ext import db

from entities.entity import Post, User, Like
from handlers.auth import AuthHandler

from datetime import datetime


class LikeBlog(AuthHandler):
    """

    """
    def get(self, post_id):
        """
        """
        user_obj = User.get_by_id(int(self.user))
        if not self.user:
            cookie_error = "Your session has expired please login again to continue!"
            self.render('login.html', error=cookie_error)
        else:
            post = Post.get_by_id(int(post_id))
            author = post.user.key().id()
            if author == int(self.user) or Like.all().filter('post =', post).filter('user =', user_obj).get() != None:
                self.redirect('/like/error')
            else:
                like = Like(post=post, user=user_obj)
                like.put()
                self.redirect("/blog/{}".format(post.slug))


class LikeError(AuthHandler):

    def get(self):
        """
        Handles error cases when unauthorized like is requested
        """
        error = "You can't like your own post & can only like a post once."
        self.render("edit_blog.html", access_error=error)