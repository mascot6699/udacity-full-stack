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


class DeleteComment(AuthHandler):

    def post(self, comment_id):
        """
        Delete the comment it has been posted by the user asking to delete it
        """
        comment = Comment.get_by_id(int(comment_id))
        post_slug = copy.deepcopy(comment.post.slug)
        if self.user:
            if comment.user.key().id() == int(self.user):
                comment.delete()
                self.redirect('/blog/{}'.format(post_slug))
            else:
                self.redirect('/comment/error')
        else:
            serror = "You must be logged in to change comments"
            self.render('login.html', error=error)


class CommentError(AuthHandler):

    def get(self):
        """
        Handles error cases when unauthorized edit/delete is requested
        """
        error = "You can only edit or delete comments that you have created."
        self.render("edit_blog.html", access_error=error)


class UpdateComment(AuthHandler):
    
    def get(self, comment_id):
        """
        Shows edit comment page
        """
        comment = Comment.get_by_id(int(comment_id))
        if self.user:
            if comment.user.key().id() == int(self.user):
                self.render("update_comment.html", comment=comment)
            else:
                self.redirect('/comment/error')
        else:
            serror = "You must be logged in to change comments"
            self.render('login.html', error=error)

    def post(self, comment_id):
        """
        """
        comment = Comment.get_by_id(int(comment_id))
        if self.user:
            if comment.user.key().id() == int(self.user):
                comment.comment = self.request.get('comment')
                comment.put()
                self.redirect('/blog/{}'.format(comment.post.slug))
            else:
                self.redirect('/comment/error')
        else:
            serror = "You must be logged in to change comments"
            self.render('login.html', error=error)
            
        