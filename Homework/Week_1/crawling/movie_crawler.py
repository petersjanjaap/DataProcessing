"""
Creates a movie class with the following attributes:
- title, runtime, genres, directors, writers, actors, ratings, number of ratings
"""
class Movie(object):

    # item objects consist of name, description and room location
    def __init__(self, title, runtime, genres, directors, writers, actors, \
                 ratings, no_ratings):
        self.title = title
        self.runtime = runtime
        self.genres = genres
        self.directors = directors
        self.writers = writers
        self.actors = actors
        self.ratings = ratings
        self.no_ratings = no_ratings
