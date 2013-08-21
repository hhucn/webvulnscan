"""
Functions described here are for python 2/3 compability and other tasks.
"""

from .compat import urlparse, urlencode, urljoin, parse_qsl

import io
import json
import sys


def read_config(config_file, parser):
    with io.open(config_file, 'r', encoding='utf-8') as f:
        values = json.load(f)

    return values['options'], values['arguments']


def write_json(obj, filename):
    if sys.version_info >= (3, 0):
        with open(filename, 'w+', encoding='utf-8') as f:
            json.dump(obj, f)
    else:
        # In Python 2.x, json.dump expects a bytestream
        with open(filename, 'wb') as f:
            json.dump(obj, f)


def write_config(filename, options, arguments):
    write_json({"options": options.__dict__, "arguments": arguments}, filename)


def modify_parameter(parameter, target_name, value):
    parameter[target_name] = value
    return parameter


def change_parameter(url, parameter, new_value):
    """ Returns a new url where the parameter is changed. """
    url_query = urlparse(url).query
    query = dict(parse_qsl(url_query))

    if query:
        for name, value in query.items():
            if name == parameter:
                query[name] = new_value

        encoded = "?" + urlencode(query)
        return urljoin(url, encoded)
    else:
        return url


def get_url_host(url):
    """ Returns the server of a name."""
    return urlparse(url).netloc


def get_page_text(page):
    for element in page.document.findall('.//*'):
        if element.text:
            yield element.text
