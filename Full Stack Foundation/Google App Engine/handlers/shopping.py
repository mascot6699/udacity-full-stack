from .base import Handler

class ShoppingListHandler(Handler):
    """
    Shopping list handler
    """
    def get(self):
        """
        Shows form back.
        """
        items = self.request.get_all("food")
        self.render("shopping_list.html", items=items)