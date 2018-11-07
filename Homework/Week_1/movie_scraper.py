"""
Jan Peters
10452125
Creates a movie class with the following attributes
- Title
- Rating
- Year of release (only a number!)
- Actors/actresses (comma separated if more than one)
- Runtime (only a number!)
"""
class Movie(object):

    # item objects consist of name, description and room location
    def __init__(self, title, rating, year, actors, runtime):
        self.title = title
        self.rating = rating
        self.year = year
        self.actors = actors
        self.runtime = runtime
