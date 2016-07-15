from .base import Handler

class IndexHandler(Handler):
    """
    Shows the top most recent 10 post in the whole site
    """
    def get(self):
        """
        """
        self.render('index.html')