import webapp2
import jinja2
import os


template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
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