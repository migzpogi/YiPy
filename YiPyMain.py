import feedparser
import re
from jinja2 import Environment, FileSystemLoader

TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader('./email'),
    trim_blocks=False
)


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


def render_template(template_filename, context):
    """
    Reads the template.html file which is how the email notification would look like
    :param template_filename:
    :param context:
    :return:
    """

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

    with open('./email/index.html', 'w') as f:
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

if __name__ == '__main__':
    ytsRSS = load_rss('https://yts.ag/rss')
    movieList = generate_movie_list(ytsRSS)
    hd = filter_movie_list(movieList)

    for x in hd:
        print(x.title)

    create_index_html(hd)
