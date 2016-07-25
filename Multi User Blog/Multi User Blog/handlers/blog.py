"""
Contains CRUD views of blogs
"""
from google.appengine.ext import db

from entities.entity import Post, User
from handlers.auth import AuthHandler

from datetime import datetime


class AddBlog(AuthHandler):
    """
    To create a new blog post
    """

    def get(self):
        """
        Renders the form for adding post
        """
        if self.user:
            self.render('add_blog.html', user=self.user)
        else:
            cookie_error = "Your session has expired please login again to continue!"
            self.render('login.html', error=cookie_error)

    def post(self):
        """
        To process ans store blog post information into database
        """
        title = self.request.get("title")
        content = self.request.get("content")
        if self.user:
            if title and content:
                user_obj = User.get_by_id(int(self.user))
                # adding publish date directly for now
                post = Post(title=title, content=content, user=user_obj, published_at=datetime.now())
                new_post = post.put()
                self.redirect("/blog/{}".format(db.get(new_post).slug))
            else:
                error = "Both title and art required for submitting !"
                self.render("add_blog.html", subject=title, content=content, error=error)
        else:
            cookie_error = "Your session has expired please login again to continue!"
            self.render('login.html', error=cookie_error)


class EditBlog(AuthHandler):
    """
    To create a new blog post
    """

    def get(self, post_id):
        """
        Renders the form for adding post
        """
        if self.user:
            post = Post.get_by_id(int(post_id))
            if not post:
                self.error(404)
            if post.user.key().id() == int(self.user):
                self.render("edit_blog.html", post=post)
            else:
                error = "You cannot edit this post."
                self.render("edit_blog.html", access_error=error)
        else:
            cookie_error = "Your session has expired please login again to continue!"
            self.render('login.html', error=cookie_error)

    def post(self, post_id):
        """
        To process ans store blog post information into database
        """
        title = self.request.get("title")
        content = self.request.get("content")

        if self.user:
            post = Post.get_by_id(int(post_id))
            if post.user.key().id() == int(self.user):
                if title and content:
                    post.title = title
                    post.content = content
                    # post.slug = post.slug
                    # TODO: should we change slug or not? else permalink wont be perament! Dig on how to fix this
                    new_post = post.put()
                    self.redirect("/blog/{}".format(db.get(new_post).slug))
                else:
                    error = "Both title and art required for submitting !"
                    self.render("edit_blog.html", post=post, error=error)
            else:
                error = "You cannot edit this post."
                self.render("edit_blog.html", access_error=error)
        else:
            self.login_redirect()


class Permalink(AuthHandler):
    """
    Blog post permalink.
    """
    def get(self, post_slug):
        is_author=False
        post = Post.all().filter("slug =", post_slug).get()
        if not post:
            self.error(404)
            return
        if self.user and post.user.key().id() == int(self.user):
            is_author = True 
        self.render('permalink.html', post=post, is_author=is_author)


class BlogList(AuthHandler):
    """
    Blog list page.
    """
    def get(self):
        posts = db.GqlQuery("SELECT * FROM Post WHERE is_draft=False ORDER BY created_at DESC LIMIT 10")
        if self.user:
            user = User.get_by_id(int(self.user))
            self.render('blog_list.html', posts=posts, username=user.username)
        else:
            self.render('blog_list.html', posts=posts)


class DeleteBlog(AuthHandler):
    """
    To delete a blog post
    """

    def get(self, post_id):
        """
        To delete a blog post, Can be done by only user who created it
        """
        if self.user:
            post = Post.get_by_id(int(post_id))
            if not post:
                self.error(404)
            if post.user.key().id() == int(self.user):
                post.delete()
                self.redirect('/')
            else:
                error = "You cannot delete this post."
                self.render("edit_blog.html", access_error=error)
        else:
            cookie_error = "Your session has expired please login again to continue!"
            self.render('login.html', error=cookie_error)