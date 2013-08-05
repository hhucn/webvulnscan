"""
Functions described here are for python 2/3 compability and other tasks.
"""

from sys import stdout, stderr

import xml.etree.ElementTree as ET
import re

try:
    from urllib.request import urlopen, build_opener, install_opener, HTTPRedirectHandler, Request
except ImportError:
    from urllib2 import urlopen, build_opener, install_opener, HTTPRedirectHandler, Request

try:
    from urllib.parse import urlparse, parse_qsl, urlunparse, urlencode
except ImportError:
    from urlparse import urlparse, parsq_qsl, urlunparse, urlencode

def find_get_parameters(url):
    """ Returns the get parameters of a given url. """ 
    if "?" in url:
        url =  url.split("?")[1]
    url_parts = parse_qsl(url)

    parameters = []
    for para in url_parts:
        parameters.extend([para[0]])

    return parameters 


def change_parameter(url, parameter, new_text):
    """ Returns a new url where the parameter is changed. """
    url_parts = list(urlparse(url))
    query = dict(parse_qsl(url_parts[4]))
    query[parameter] = new_text
    
    url_parts[4] = urlencode(query)
    return urlunparse(url_parts)
    

def get_plain_text(url, parameters=None):
    """ 
    Returns the plain_text of the site behind url. Returns "" if
    Content-Type  != "text/html"
    """
    redirect_handler = HTTPRedirectHandler()

    opener = build_opener(redirect_handler)

    install_opener(opener)


    if parameters == None:
        request = Request(url)
    else:
        data = urlencode(parameters)
        request = Request(url, data.encode('utf-8'))

    response = opener.open(request)

    content_type = response.info()["Content-Type"]


    # Determine Content-Type
    split_content = content_type.split(";")
    if len(split_content) == 0:
        pass
    else:
        content_type = split_content[0]
    

    if content_type == "text/html":
        return response.read().decode("utf-8")
    else:
        return None

def get_page(url):
    """ Returns a xml.etree.ElementTree object containing the document. """
    plain_text = get_plain_text(url)

    # Check for HTTP-Error
    if plain_text == None:
        return None

    # REMOVE DOCTYPE
    if plain_text.startswith("<!doctype"):
        _, _, plain_text  = plain_text.partition('>')

    # Bad Solution for removing entities
    decoded_html = re.sub('&([^;]+);', '', plain_text)

    try:
        root = ET.fromstring(decoded_html)
    except ET.ParseError as error:
        print("Syntax error on Line " + str(error.position[0]) +
                " Column " + str(error.position[1]) + ":")
        print(decoded_html.split('\n')[error.position[0]])
        exit(2)

    return root 
