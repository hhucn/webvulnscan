""" Main module provides crawling functions and user interface """

from utils import find_get_parameters
from crawling import crawl
from attacks import drive_all


def crawl_page(url, white_list):
    """ Crawls url for its forms and links and attacks all. """
    for site, form in crawl(url, white_list):
        drive_attack(site, form)


def drive_attack(url, url_forms):
    """ Initates attack on the given target """
    url_parameters = find_get_parameters(url)
    drive_all(url, url_parameters, url_forms)
