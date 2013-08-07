""" Main module provides crawling functions and user interface """

from optparse import OptionParser

from .attacks import drive_all
from .crawling import crawl, forms_on_site
from .utils import find_get_parameters, get_plain_text, get_page, get_url_host


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

    options, arguments = parser.parse_args()

    if len(arguments) < 1:
        parser.error('Invalid amount of arguments')

    if options.auth is not None:
        if options.auth_data is not None:
            post_data = {}

            for field in options.auth_data:
                name, _, value = field.partition('=')
                post_data.update({name: value})

            get_plain_text(options.auth, post_data)

    for target in arguments:
        host = get_url_host(target)
        if host not in options.white_list:
            options.white_list.update({host})

        if options.no_crawl:
            site = get_page(target)
            if site is not None:
                forms = forms_on_site(target, site)
                drive_attack(target, forms)
        else:
            crawl_page(target, options.white_list)


def crawl_page(url, white_list):
    """ Crawls url for its forms and links and attacks all. """
    for site, forms in crawl(url, white_list):
        drive_attack(site, forms)


def drive_attack(url, url_forms):
    """ Initates attack on the given target """
    url_parameters = find_get_parameters(url)
    drive_all(url, url_parameters, url_forms)
