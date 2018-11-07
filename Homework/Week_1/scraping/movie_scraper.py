"""
Jan Peters
10452125
creates a movie class with the following attributes
- title
- rating
- year of release
- actors/actresses
- runtime
"""
class Movie(object):

    # item objects consist of name, description and room location
    def __init__(self, title, rating, year, actors, runtime):
        self.title = title
        self.rating = rating
        self.year = year
        self.actors = actors
        self.runtime = runtime
