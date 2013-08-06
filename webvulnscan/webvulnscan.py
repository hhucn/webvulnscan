""" Main module provides crawling functions and user interface """

from utils import find_get_parameters
from crawling import crawl, forms_on_site
from attacks import drive_all


def crawl_page(url, white_list):
    """ Crawls url for its forms and links and attacks all. """
    for site, page in crawl(url, white_list):
        if site is not None and page is not None:
            forms = {x: y for x, y in forms_on_site(site, page)}
            drive_attack(site, forms)


def drive_attack(url, url_forms):
    """ Initates attack on the given target """
    url_parameters = find_get_parameters(url)
    drive_all(url, url_parameters, url_forms)
