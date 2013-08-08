"""
Functions described here are for python 2/3 compability and other tasks.
"""

from .EtreeParser import EtreeParser
from logging import getLogger

import xml.etree.ElementTree as ET

try:
    from urllib.request import build_opener, install_opener, \
        HTTPRedirectHandler, Request, HTTPCookieProcessor, HTTPError, \
        URLError
except ImportError:
    from urllib2 import build_opener, install_opener, \
        HTTPRedirectHandler, Request, HTTPCookieProcessor, HTTPError, \
        URLError

try:
    from urllib.parse import urlparse, parse_qsl, urlunparse, urlencode
except ImportError:
    from urlparse import urlparse, parse_qsl, urlunparse
    from urllib import urlencode

try:
    from http.cookiejar import CookieJar
except ImportError:
    from cookielib import CookieJar

log = getLogger(__name__)


# One Cookiejar for all - this must me done better.
global cookie_jar
cookie_jar = CookieJar()


def find_get_parameters(url):
    """ Returns the get parameters of a given url. """
    if "?" in url:
        url = url.split("?")[1]
    url_parts = parse_qsl(url)

    parameters = []
    for para in url_parts:
        parameters.append(para[0])

    return parameters

def find_parameter_values(url):
    """ Find the values of the parameters of the URL """
    if "?" in url:
        url = url.split("?")[1]
    
    url_parts = parse_qsl(url)

    for parameter in url_parts:
        yield parameter[1]


def change_parameter(url, parameter, new_value):
    """ Returns a new url where the parameter is changed. """
    url_parts = list(urlparse(url))
    query = parse_qsl(url_parts[4])
    for i in range(len(query)):
        entry = query[i]
        if entry[0] == parameter:
            query[i] = (entry[0], new_value)

    url_parts[4] = urlencode(query)
    return urlunparse(url_parts)


def get_url_host(url):
    """ Returns the server of a name."""
    parsed = urlparse(url)
    return parsed.netloc


def get_plain_text(url, parameters=None, cookies=cookie_jar):
    """
    Returns the plain_text of the site behind url. Returns "" if
    Content-Type  != "text/html"
    """
    redirect_handler = HTTPRedirectHandler()

    opener = build_opener(redirect_handler)
    opener = build_opener(HTTPCookieProcessor(cookies))
    install_opener(opener)

    if parameters is None:
        request = Request(url)
    else:
        data = urlencode(parameters)
        request = Request(url, data.encode('utf-8'))

    # TODO Socket error behandlung.
    try:
        response = opener.open(request)
    except HTTPError as error:
        if error.code == 400:
            return None
        else:
            log.warning("Warning: HTTP Code " + str(error.code) +
                        " received from " + url)
            raise

    except URLError as error:
        log.exception(url + " is not reachable!")
        raise

    headers = response.info()

    if "Content-Type" in headers:
        content_type = headers["Content-Type"]

        # Determine Content-Type
        split_content = content_type.split(";")
        if split_content is not None:
            content_type = split_content[0]

        if content_type == "text/html":
            return response.read().decode("utf-8")
        else:
            return None
    else:
        return response.read().decode("utf-8")


def get_page(url):
    """ Returns a xml.etree.ElementTree object containing the document. """
    plain_text = get_plain_text(url)

    # Check for HTTP-Error
    if plain_text is None:
        return None

    try:
        parser = EtreeParser(url)
        root = ET.fromstring(plain_text, parser)
    except ET.ParseError as error:
        log.exception("Syntax error on Line " + str(error.position[0]) +
                      " Column " + str(error.position[1]) + ":")
        log.exception(plain_text.split('\n')[error.position[0]])
        raise

    return root
