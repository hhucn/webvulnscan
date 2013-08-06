""" This module provides the userinterface. """
from utils import get_plain_text, get_page, get_url_host
from webvulnscan import crawl_page, form_crawl, drive_attack
from optparse import OptionParser
from ast import literal_eval


def main():
    """ The main function. """
    parser = OptionParser(usage="usage: %prog [options] http(s)://target/")
    parser.add_option('--no-crawl', action="store_true", dest="no_crawl",
                      help="DO NOT search for links on the target")
    parser.add_option('--whitelist', '-w', default=set(), dest="white_list",
                      help="Hosts which are allowed to be crawled.")
    parser.add_option('--auth', '-a', default=None, dest="auth",
                      help="Optional: List with URL of auth post target and " +
                           "values")

    options, arguments = parser.parse_args()
    target = arguments[0]

    if len(arguments) != 1:
        parser.error("Invalid amount of arguments")

    if options.auth is not None:
        auth = literal_eval(options.auth)
        get_plain_text(auth[0], auth[1])

    host = get_url_host(target)
    if host not in options.white_list:
        options.white_list.update({host})

    if options.no_crawl:
        site = get_page(target)
        if site is not None:
            forms = form_crawl(site)
            drive_attack(target, forms)
    else:
        crawl_page(target, options.white_list)


if __name__ == '__main__':
    main()
