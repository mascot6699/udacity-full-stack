"""
Generates the list of movies object.
"""

from .media import Movie
import csv


def get_movies(filename):
    """
    pulls movie data from csv and returns a list a Movie objects
    """
    movies = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for movie in reader:
            movies.append(Movie(title=movie['name'], image_url=movie['image_url'], youtube_url=movie['youtube_url']))
    return movies