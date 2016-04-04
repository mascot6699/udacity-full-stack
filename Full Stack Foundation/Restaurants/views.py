import utils


def get_restaurant_list_template():
    """
    :return: message that lists the name of the restaurants
    """
    restaurants = utils.get_restaurants()
    message = "<html><body>"
    for restaurant in restaurants:
        message += restaurant.name
        message += "</br>"
        message += "<a href ='#'>Edit</a>   "
        message += "<a href ='#'>Delete</a>"
        message += "</br></br></br>"
    message += "</body></html>"
    return message