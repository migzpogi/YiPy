import argparse
import sys

def determine_modes(args):
    """

    :param args:
    :return:
    """

    print args.console_status
    print args.file_status
    print args.email_status

if __name__ == '__main__':
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
        determine_modes(args)
    else:
        parser.print_help()
        parser.exit()
