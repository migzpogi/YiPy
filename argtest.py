import argparse
import sys
import logging.config
from ConfigParser import ConfigParser
import feedparser

def run_commands(args):
    """
    Runs the application with the specified commands
    :param args:
    :return:
    """

    if args.console_status:
        print "Console Mode"
    if args.file_status:
        print "File Mode"
    if args.email_status:
        print "Email mode"


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
    except Exception as e:
        log.warn(e)

    return feed

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

    # load the rss feed
    ytsRSS = load_rss('https://yts.ag/rss')

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
