from .base import Handler

class IndexPageHandler(Handler):
    """
    """
    def get(self):
        """
        Landing or Index page handler
        """
        self.render('index.html')
