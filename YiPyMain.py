#!/usr/bin/env python
import argparse
from configparser import ConfigParser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import feedparser
from jinja2 import Environment, FileSystemLoader
import logging.config
import re
import sys
import smtplib
import time


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


def send_email(config_object):
    """
    Sends the email notification
    :return:
    """

    config_object = Config(config_object)

    msg = MIMEMultipart('alternative')
    msg['From'] = config_object.emailfrom
    msg['To'] = config_object.emailto
    msg['Subject'] = config_object.emailsubject

    with open('./email/index.html', 'r') as f:
        html = f.read()

    attch = MIMEText(html, 'html')
    msg.attach(attch)

    try:
        e = smtplib.SMTP('smtp.gmail.com', 587)
        e.starttls()
        e.login(config_object.smtpuser, config_object.smtppass)
        e.sendmail(config_object.emailfrom, config_object.emailto, msg.as_string())
        e.quit()
        print("Email sent")
    except:
        print("Email not sent")


def render_template(template_filename, context):
    """
    Reads the template.html file which is how the email notification would look like
    :param template_filename:
    :param context:
    :return:
    """

    # location of the template file
    TEMPLATE_ENVIRONMENT = Environment(
        autoescape=False,
        loader=FileSystemLoader('./email'),
        trim_blocks=False
    )

    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)


def create_index_html(movie_list):
    """
    Created the index.html which is the body of the email notification
    :param movie_list:
    :return:
    """
    context = {
        'response': movie_list
    }

    with open('./email/index.html', 'wb') as f:
        html = render_template('template.html', context)
        f.write(html.encode('utf-8'))


def load_rss(rss_feed):
    """
    Reads the RSS feed of YTS
    :param rss_feed:
    :return: feedparser.FeedParserDict
    """

    return feedparser.parse(rss_feed)


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


def filter_movie_list(movie_list, quality='1080p'):
    """
    Filters the given movie list according to the passed parameters
    :param quality:
    :return:
    """

    filtered_list = []
    for idx, m in enumerate(movie_list):
        if m.quality == quality:
            filtered_list.append(m)

    return filtered_list


def __print_ascii():
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

  Version 1.0.0                         
    """)


def __handle_args():
    """
    Handles the arguments passed by the user. Used mainly for mode selection.
    :return: argParse.ArgumentParser()
    """
    parser = argparse.ArgumentParser(
        description='Welcome to YiPy, an application that gets the most recent updates '
                    'of YTS. Chooose from the following modes below:')

    parser.add_argument('-c', '--comandline', action='store_true', default=False,
                        dest='bool_cli', help='Displays the output in the command line '
                                              'interface.')

    parser.add_argument('-f', '--file', action='store_true', default=False,
                        dest='bool_file', help='Writes the output in a text file.')

    parser.add_argument('-e', '--email', action='store_true', default=False,
                        dest='bool_email', help='Sends the output ito an email address.')

    return parser


def __init_logging():
    """
    Initialize logging function.
    :return: logging.getLogger()
    """

    log = logging.getLogger("YiPy")
    logging.config.fileConfig(
        disable_existing_loggers=False,
        fname='./log/logconfig.ini',
        defaults={'logfilename': './log/yipytrace.log'})

    return log

def __init_config():
    """
    Initialize config function
    :return: ConfigParser()
    """

    config = ConfigParser()
    config.read('./config/settings.ini')

    return config


def __run_cli_mode():
    """
    Runs the CLI mode of the application which displays the output on the command line
    interface
    :return:
    """

    logger.info("CLI MODE")

    ytsRSS = load_rss(cfg.get('rssfeed', 'rss'))
    movie_list = generate_movie_list(ytsRSS)
    filtered = filter_movie_list(movie_list, quality=cfg.get('filters', 'quality'))

    for movies in filtered:
        logger.info(movies.cleantitle + '---' + movies.imdb) 

def __run_file_mode():
    """
    Runs the File mode of the application which writes the output on a text file
    :return:
    """

    logger.info("FILE MODE -- Coming Soon!")


def __run_email_mode():
    """
    Runs the Email mode of the application which sends the output to an email address
    :return:
    """

    logger.info("EMAIL MODE -- Coming Soon!")


if __name__ == '__main__':

    # show ascii art
    __print_ascii()

    # initialize logging
    logger = __init_logging()

    # initialize config
    cfg = __init_config()

    # initialize argument parser
    parser = __handle_args()
    results = parser.parse_args()

    # display argparse help if no argument is passed
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    # mode checking
    cli_mode = results.bool_cli
    file_mode = results.bool_file
    email_mode = results.bool_email

    if cli_mode:
        __run_cli_mode()
    if file_mode:
        __run_file_mode()
    if email_mode :
        __run_email_mode()


    #
    # log.info('YiPy started...')
    #
    # # load config
    # config = SafeConfigParser()
    # config.read('./config/settings.ini')
    #
    # # load the rss feed
    # log.info('Parsing RSS feed...')
    # ytsRSS = load_rss('https://yts.ag/rss')
    # log.info('RSS feed parsed...')
    #
    # # create a movie list that is 1080p in quality
    # log.info("Listing recent uploads with 1080p resolution...")
    # movieList = generate_movie_list(ytsRSS)
    # hd = filter_movie_list(movieList)
    #
    # for movies in hd:
    #     log.info(movies.cleantitle)
    #
    #
    # # send email
    # create_index_html(hd)
    # # send_email(config)

