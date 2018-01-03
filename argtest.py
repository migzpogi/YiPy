import argparse
import sys
import logging.config
from ConfigParser import ConfigParser
import feedparser
import re


class Config(object):
    """
    Object representation of the config file
    """

    def __init__(self, config):
        self.config = config
        self.smtpuser = self.config.get('smtp', 'username')
        self.smtppass = self.config.get('smtp', 'password')
        self.emailfrom = self.config.get('email', 'from')
        self.emailto = self.config.get('email', 'to')
        self.emailsubject = self.config.get('email', 'subject')


class Movie(object):
    """
    Object representation of a movie entry
    """

    def __init__(self, movie):
        self.movie = movie
        self.__set_information()

    def __set_information(self):
        """
        Sets the various information of the movie such as title, ratings, etc.
        :return:
        """

        # title
        self.title = self.movie.title

        # clean title: strips the quality part section of the title
        self.cleantitle = self.title[:-8]

        # quality
        if '[720p]' in self.title:
            self.quality = '720p'
        elif '[1080p]' in self.title:
            self.quality = '1080p'
        elif '[3D]' in self.title:
            self.quality = '3D'
        else:
            self.quality = None

        # summary
        self.summary = self.movie.summary

        # imdb rating
        search = re.search(r'IMDB Rating: [0-9].[0-9][/]10', self.movie.summary)
        self.imdb = search.group()

        # synopsis
        parts = self.summary.split('>')  # split the summary part with '>' as the delimiter
        last_part = parts[len(parts)-1]  # get only the last part
        self.synopsis = last_part

        # download link
        self.downloadlink = self.movie.links[1]['href']


def print_ascii():
    """
    Prints an ASCII art of the project name
    :return:
    """
    print("""
 _     _ _____ ______  _     _ 
| |   | (_____|_____ \| |   | |
| |___| |  _   _____) ) |___| |
 \_____/  | | |  ____/ \_____/ 
   ___   _| |_| |        ___   
  (___) (_____)_|       (___)  

  Version 1.0                         
    """)


def load_rss(rss_feed):
    """
    Reads the RSS feed of YTS
    :param rss_feed:
    :return: feedparser.FeedParserDict
    """
    feed = None

    try:
        feed = feedparser.parse(rss_feed)
        log.info('RSS feed parsed!')
    except Exception as e:
        log.warn(e)

    return feed


def generate_movie_list(yts_rss):
    """
    Given a parsed YTS RSS, this function will generate a list of movies using the Movie class
    :param yts_rss:
    :return: List of Movie objects
    """

    movie_list = []
    for idx, m in enumerate(yts_rss.entries):
        movie_list.append(Movie(m))

    return movie_list


def filter_movie_list(movie_list, quality):
    """
    Filters the given movie list according to the passed parameters
    :param movie_list
    :param quality:
    :return:
    """

    filtered_list = []
    for idx, m in enumerate(movie_list):
        if m.quality == quality:
            filtered_list.append(m)

    return filtered_list


def mode_console(parsed_rss):
    """

    :param parsed_rss:
    :return:
    """

    log.info('Running YiPy in Console Mode')
    log.info('***** RECENT UPLOADS START *****')

    movie_list = generate_movie_list(parsed_rss)
    filtered = filter_movie_list(movie_list, quality=config.get('filters', 'quality'))

    for movies in filtered:
        log.info(movies.cleantitle + ' -- ' + movies.imdb)

    log.info('***** RECENT UPLOADS END *****')


def run_commands(args):
    """
    Runs the application with the specified commands
    :param args:
    :return:
    """

    # load the rss feed
    ytsRSS = load_rss(config.get('rssfeed', 'rss'))

    if args.console_status:
        mode_console(ytsRSS)
    if args.file_status:
        print "File Mode"
    if args.email_status:
        print "Email mode"


if __name__ == '__main__':
    # initialize logging
    log = logging.getLogger("YiPy")
    logging.config.fileConfig(
        disable_existing_loggers=False,
        fname='./log/logconfig.ini',
        defaults={'logfilename': './log/yipytrace.log'})
    log.info('YiPy started. Reading config...')

    # load config
    config = ConfigParser()
    config.read('./config/settings.ini')
    log.info('Config loaded. Parsing the RSS feed...')

    # get the passed arguments
    parser = argparse.ArgumentParser(
        description="Please choose from the following modes:")

    parser.add_argument('--console', '-c', default=False, action='store_true',
                        dest='console_status', help='Shows the output in the console.')
    parser.add_argument('--file', '-f', default=False, action='store_true',
                        dest='file_status', help='Writes the output in a text file.')
    parser.add_argument('--email', '-e', default=False, action='store_true',
                        dest='email_status', help='Sends the output to an email.')

    if len(sys.argv) > 1:
        args = parser.parse_args()
        run_commands(args)

    else:
        parser.print_help()
        parser.exit()
