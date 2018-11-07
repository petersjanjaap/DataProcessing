#!/usr/bin/env python
# Name: Jan Peters
# Student number: 10452125
"""
this script scrapes IMDB and outputs a CSV file with highest rated movies.
"""

# imports libraries
import re
import csv
from movie_scraper import Movie
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

TARGET_URL = "https://www.imdb.com/search/title?title_type=feature&release_date=2008-01-01,2018-01-01&num_votes=5000,&sort=user_rating,desc"
BACKUP_HTML = 'movies.html'
OUTPUT_CSV = 'movies.csv'


def extract_movies(dom):
    """
    extract all relevant movie information on htmlpage
    """
    # parse the HTML file into a DOM representation
    boxes = dom.div.findAll("div",{"class":"lister-item-content"})

    # dictionary for all movies
    all_movies = {}

    # iterate over all boxes containing movie info
    for box in boxes:

        # extracts title rating and year
        title = box.h3.a.string
        rating = box.find("strong").string
        year = box.find("span", {"class":"lister-item-year text-muted unbold"})\
                        .string

        #strips year from non-numeric characters
        for char in year:
            if char not in '1234567890':
                year = year.replace(char,'')

        # extracts actors and stores names in string
        cast = box.find_all(href=re.compile("adv_li_st"))
        actors = ", "
        for actor in cast:
            actors = actors + actor.string + ", "
        actors = actors[:-2]

        # stores runtime as number of minutes
        runtime = box.find("span", {"class":"runtime"}).string[:-4]

        # creates movie object and adds to dictionary
        movie = Movie(title, rating, year, actors, runtime)
        all_movies[title] = movie

    # returns dictionary containing all movie objects
    return all_movies


def save_csv(outfile, movies):
    """
    output a CSV file containing highest rated movies.
    """
    writer = csv.writer(outfile)
    writer.writerow(['Title', 'Rating', 'Year', 'Actors', 'Runtime'])

    # writes all movie elements to seperate cells in row
    for movie in movies.values():
        writer.writerow([movie.title, movie.rating, movie.year, movie.actors, \
        movie.runtime])


def simple_get(url):
    """
    attempts to get the content at `url` by making an HTTP GET request.
    if the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        print('The following error occurred during HTTP GET request to\
                0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


if __name__ == "__main__":
    # get HTML content at target URL
    html = simple_get(TARGET_URL)

    # save a copy to disk in the current directory, this serves as an backup
    # of the original HTML, will be used in grading.
    with open(BACKUP_HTML, 'wb') as f:
        f.write(html)
    dom = BeautifulSoup(html, 'html.parser')

    # extract the movies (using the function you implemented)
    movies = extract_movies(dom)

    # write the CSV file to disk (including a header)
    with open(OUTPUT_CSV, 'w', newline='') as output_file:
        save_csv(output_file, movies)
