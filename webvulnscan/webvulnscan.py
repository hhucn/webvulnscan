""" Main module provides crawling functions and user interface """

from utils import get_page, find_get_parameters, get_url_host
from attacks import drive_all

try:
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import HTTPError

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


def crawl(document):
    """ Takes a html string and returns a list of strings. """
    link_list = []
    for link in document.findall('.//a[@href]'):
        link_target = link.attrib.get('href')
        link_list.append(link_target)

    return link_list


def form_crawl(document):
    """
    Takes a html string a dictionariy with the different forms
    and their parameters.
    """
    form_dict = {}
    for form in document.findall('.//form[@action]'):
        target = form.attrib.get('action')
        input_list = {}

        for sub_element in form:
            if sub_element.tag == "input":
                input_name = sub_element.attrib.get('name')
                input_type = sub_element.attrib.get('type')
                input_value = sub_element.attrib.get('value')
                input_place = sub_element.attrib.get('placeholder')

                if input_value == "" and input_place != "":
                    input_value = input_place

                if input_type != "submit":
                    input_list.update({input_name: input_value})

        form_dict.update({target: input_list})

    return form_dict


def crawl_page(url, white_list, already_visited=None):
    """ Crawls url for its forms and links and attacks all. """
    if already_visited is None:
        already_visited = set()

    if get_url_host(url) not in white_list:
        return

    try:
        html = get_page(url)
    except HTTPError:
        return

    if html is None:
        drive_attack(url, set())
    else:
        significant_forms = dict()
        forms = form_crawl(html)
        for form in forms:
            form_link = urljoin(url, form)
            if form_link not in already_visited:
                already_visited.update({form_link})
                significant_forms.update({form_link: forms[form]})

        for link in crawl(html):
            link = urljoin(url, link)
            if link not in already_visited:
                already_visited.update({link})
                crawl_page(link, white_list, already_visited)

        drive_attack(url, significant_forms)


def drive_attack(url, url_forms):
    """ Initates attack on the given target """
    url_parameters = find_get_parameters(url)
    drive_all(url, url_parameters, url_forms)
