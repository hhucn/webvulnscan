"""
Functions described here are for python 2/3 compability and other tasks.
"""

from .compat import urlparse, urlencode, urljoin, parse_qsl

import json


def read_config(config_file, parser):
    with open(config_file, 'r', encoding='utf-8') as f:
        values = json.load(f)

    return values['options'], values['arguments']


def write_config(config_file, options, arguments):
    with open(config_file, 'w+', encoding='utf-8') as f:
        json.dump({"options": options.__dict__, "arguments": arguments}, f)


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
