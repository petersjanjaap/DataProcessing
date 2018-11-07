#!/usr/bin/env python
# Name: Jan Peters
# Student number: 10452125
"""
this script crawls the IMDB top 250 movies.
"""

import os
import csv
import codecs
import errno
import re

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from movie_crawler import Movie

# global constants
TOP_250_URL = 'http://www.imdb.com/chart/top'
OUTPUT_CSV = 'top250movies.csv'
SCRIPT_DIR = os.path.split(os.path.realpath(__file__))[0]
BACKUP_DIR = os.path.join(SCRIPT_DIR, 'HTML_BACKUPS')

# --------------------------------------------------------------------------
# Utility functions (no need to edit):


def create_dir(directory):
    """
    create directory if needed.
    args:
        directory: string, path of directory to be made
    note: the backup directory is used to save the HTML of the pages you
        crawl.
    """

    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno == errno.EEXIST:
            # Backup directory already exists, no problem for this script,
            # just ignore the exception and carry on.
            pass
        else:
            # All errors other than an already existing backup directory
            # are not handled, so the exception is re-raised and the
            # script will crash here.
            raise


def save_csv(filename, rows):
    """
    save CSV file with the top 250 most popular movies on IMDB.
    args:
        filename: string filename for the CSV file
        rows: list of rows to be saved (250 movies in this exercise)
    """
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'title', 'runtime', 'genre(s)', 'director(s)', 'writer(s)',
            'actor(s)', 'rating(s)', 'number of rating(s)'
        ])
        # writes all movie information to file
        writer.writerows(rows)


def make_backup(filename, html):
    """
    save HTML to file.
    args:
        filename: absolute path of file to save
        html: (unicode) string of the html file
    """

    with open(filename, 'wb') as f:
        f.write(html)


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
        print('The following error occurred during HTTP GET request to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    returns true if the response seems to be HTML, false otherwise
    and content_type is not None
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type.find('html') > -1)


def main():
    """
    crawl the IMDB top 250 movies, save CSV with their information.
    note:
        this function also makes backups of the HTML files in a sub-directory
        called HTML_BACKUPS (those will be used in grading).
    """

    # Create a directory to store copies of all the relevant HTML files (those
    # will be used in testing).
    print('Setting up backup dir if needed ...')
    create_dir(BACKUP_DIR)

    # Make backup of the IMDB top 250 movies page
    print('Access top 250 page, making backup ...')
    top_250_html = simple_get(TOP_250_URL)
    top_250_dom = BeautifulSoup(top_250_html, "lxml")

    make_backup(os.path.join(BACKUP_DIR, 'index.html'), top_250_html)

    # extract the top 250 movies
    print('Scraping top 250 page ...')
    url_strings = scrape_top_250(top_250_dom)

    # grab all relevant information from the 250 movie web pages
    rows = []
    for i, url in enumerate(url_strings):  # Enumerate, a great Python trick!
        print('Scraping movie %d ...' % i)

        # Grab web page
        movie_html = simple_get(url)

        # Extract relevant information for each movie
        movie_dom = BeautifulSoup(movie_html, "lxml")
        movie = scrape_movie_page(movie_dom)
        movie = [movie.title, movie.runtime, movie.genres,movie.directors, \
            movie.writers, movie.actors,movie.ratings, movie.no_ratings]
        rows.append(movie)

        # Save one of the IMDB's movie pages (for testing)
        if i == 83:
            html_file = os.path.join(BACKUP_DIR, 'movie-%03d.html' % i)
            make_backup(html_file, movie_html)

    # Save a CSV file with the relevant information for the top 250 movies.
    print('Saving CSV ...')
    save_csv(os.path.join(SCRIPT_DIR, 'top250movies.csv'), rows)


# --------------------------------------------------------------------------
# Functions to adapt or provide implementations for:

def scrape_top_250(soup):
    """
    scrape the IMDB top 250 movies index page.
    args:
        soup: parsed DOM element of the top 250 index page
    returns:
        A list of strings, where each string is the URL to a movie's page on
        IMDB, note that these URLS must be absolute (i.e. include the http
        part, the domain part and the path part).
    """

    # obtains all parts of webpage containing movie url
    boxes = soup.div.findAll("td",{"class":"titleColumn"})
    movie_urls = []

    # sitename to obtain full link
    site = "https://www.imdb.com"

    # iterates over all url's to movies on html page
    for box in boxes:
        url = site + (box.a.get('href'))
        movie_urls.append(url)

    # returns a list containing all movie urls
    return movie_urls


def scrape_movie_page(dom):
    """
    scrape the IMDB page for a single movie
    args:
        dom: BeautifulSoup DOM instance representing the page of 1 single
            movie.
    returns:
        a list of strings representing the following (in order): title, year,
        duration, genre(s) (semicolon separated if several), director(s)
        (semicolon separated if several), writer(s) (semicolon separated if
        several), actor(s) (semicolon separated if several), rating, number
        of ratings.
    """
    # extracts title, runtime, rating, no_ratings and genres from header
    header = dom.find("div", {"class":"title_block"})
    title = dom.find(id="ratingWidget").find("strong").string
    runtime = header.find("time").string.strip()
    rating = header.find(itemprop=re.compile("ratingValue")).string
    no_ratings = header.find("span", {"class":"small"}).string

    # takes genres from header file and removes release date element
    genres_list = header.find("div", {"class":"subtext"}).find_all("a")
    genres_list.pop()

    # genres are stored as string value
    genres = ""
    for genre in genres_list:
        genres = genres + str(genre.string) + ", "
    genres = genres[:-2]

    # from movie info directors, writers and actors are extracted
    movie_info = dom.find_all("div", {"class":"credit_summary_item"})
    directors = movie_info[0].find("a").string
    writers = movie_info[1].find("a").string
    actors = movie_info[2].find("a").string

    # adds a movie object
    movie = Movie(title, runtime, genres, directors, writers\
                              ,actors, rating, no_ratings)

    # returns movie object
    return movie

if __name__ == '__main__':
    main()  # call into the progam
