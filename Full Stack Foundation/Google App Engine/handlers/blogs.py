from .base import Handler
from entities.entity import Post

from google.appengine.ext import db


class NewBlogHandler(Handler):
    """
    New blog post add
    """
    def render_newpost(self, subject="", content="", error=""):
        self.render('new-blog.html', subject=subject, content=content,
                    error=error)

    def get(self):
        self.render_newpost()

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content').replace('\n', '<br>')

        if subject and content:
            p = Post(subject=subject, content=content)
            p.put()
            post_id = str(p.key().id())
            self.redirect('/blog/%s/' % post_id)
        else:
            error = "Please add both a title and a post!"
            self.render_newpost(subject, content, error)


class Permalink(Handler):
    """
    Blog post permalink.
    """
    def get(self, post_id):
        post = Post.get_by_id(int(post_id))

        if not post:
            self.error(404)
            return
        self.render('permalink.html', post=post)


class BlogListHandler(Handler):
    """
    Blog list page.
    """
    def get(self):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created_at DESC LIMIT 10")
        self.render('blog.html', posts=posts)