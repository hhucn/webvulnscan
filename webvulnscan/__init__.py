""" Main module provides crawling functions and user interface """

from optparse import OptionParser
from logging import getLogger, StreamHandler

#from .attacks import drive_all
from .crawler import Crawler
from .client import Client
from .utils import get_url_host
from .attacks import drive_all, AttackList

EXIT_CODE = 0


def capture_warning():
    """ When called, sets EXIT_CODE to 1"""
    global EXIT_CODE
    EXIT_CODE = 1


class LogHandler(StreamHandler):
    def __init__(self, stream=None):
        StreamHandler.__init__(self)
        # Using Monkeypatching to use old function
        self.real_emit = self.emit
        self.emit = self.handle_emit
        self.log_entrys = set()

    def handle_emit(self, record):
        msg = self.format(record)
        if "Vulnerability" in msg:
            capture_warning()

        if msg not in self.log_entrys:
            self.real_emit(record)
            self.log_entrys.update({msg})


def exit_main():
    """ Returns exit_code, is used for logging. """
    exit(EXIT_CODE)


log = getLogger(__name__)


def main():
    """ The main function. """
    parser = OptionParser(usage='usage: %prog [options] http(s)://target/ '
                                '[http(s)://another.target/]')
    parser.add_option('--no-crawl', action='store_true', dest='no_crawl',
                      help="DO NOT search for links on the target")
    parser.add_option('--whitelist', default=set(), dest="white_list",
                      help="Hosts which are allowed to be crawled.")
    parser.add_option('--auth',  default=None, dest="auth",
                      help="Post target for authentification")
    parser.add_option('--auth-data',  dest='auth_data',
                      action='append', type='str')
    parser.add_option('--blacklist', default=[], dest="blacklist",
                      action="append")
    parser.add_option('--verbose', '-v', default=None, dest="verbose",
                      action="store_true")

    # Options for scanning for specific vulnerabilities.
    for attack in AttackList():
        parser.add_option('--' + attack.name, dest=attack.name,
                          action="store_true", default=False)

    options, arguments = parser.parse_args()

    attacks = []

    for attack in AttackList():
        if attack.name in options.__dict__:
            if options.__dict__[attack.name]:
                attacks.extend([attack])

    if len(attacks) == 0:
        attacks = AttackList()

    log.addHandler(LogHandler())

    if len(arguments) < 1:
        parser.error('Invalid amount of arguments')

    client = Client()

    if options.auth is not None:
        if options.auth_data is not None:
            post_data = {}

            for field in options.auth_data:
                name, _, value = field.partition('=')
                post_data.update({name: value})

            _, text, _ = client.download(options.auth, post_data)
            # This is a little hack...
            text = str(text)

    for target in arguments:
        host = get_url_host(target)
        if host not in options.white_list:
            options.white_list.update({host})

        if options.no_crawl:
            page = client.download_page(target)
            if page is not None:
                drive_all(page, attacks, client)
        else:
            for link in Crawler(target, options.white_list, client,
                                options.blacklist):
                if options.verbose:
                    print("Scanning " + link.url)
                drive_all(link, attacks, client)

    exit_main()
