"""
Functions described here are for python 2/3 compability and other tasks.
"""

from sys import stdout, stderr

import xml.etree.ElementTree as ET
import re

try:
    from urllib.request import urlopen 
except ImportError:
    from urllib2 import urlopen

def get_plain_text(url):
    """ 
    Returns the plain_text of the site behind url. Returns "" if
    Content-Type  != "text/html"
    """
    response = urlopen(url)
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
