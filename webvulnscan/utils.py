"""
Functions described here are for python 2/3 compability and other tasks.
"""

from .compat import urlparse, urlencode, urljoin, parse_qsl

import io
import json
import re
import sys


def read_config(config_file, parser):
    with io.open(config_file, 'r', encoding='utf-8') as f:
        values = json.load(f)

    return values['options'], values['arguments']


def write_json(obj, filename, **kwargs):
    if filename == u'-':
        out = sys.stdout
    else:
        if sys.version_info >= (3, 0):
            out = open(filename, 'w+', encoding='utf-8')
        else:
            # In Python 2.x, json.dump expects a bytestream
            out = open(filename, 'wb')

    with out:
        json.dump(obj, out, **kwargs)


def write_config(filename, options, arguments):
    options_dict = options.__dict__.copy()
    del options_dict['write_config']
    del options_dict['read_config']
    write_json({"options": options_dict, "arguments": arguments}, filename,
               indent=4)


def modify_parameter(parameters, target_name, value):
    res = parameters.copy()
    res[target_name] = value
    return res


def change_parameter(url, parameter, new_value):
    """ Returns a new url where the parameter is changed. """
    url_query = urlparse(url).query
    query = dict(parse_qsl(url_query))

    if query:
        for name, _ in query.items():
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
    if page.document.text:
        yield page.document.text

    for element in page.document.findall('.//*'):
        if element.text:
            yield element.text


def attack(searchfunc=None):
    if searchfunc is None:
        searchfunc = lambda page: [(page,)]

    def run(cls, client, log, page):
        for s in cls.search(page):
            cls.attack(client, log, *s)

    def decorator(attackfunc):
        return type(attackfunc.__name__, (object,), {
            'attack': staticmethod(attackfunc),
            'search': staticmethod(searchfunc),
            '__new__': run,
        })
    return decorator


def could_be_secret(s):
    return re.match(r'^[0-9a-fA-F$!]+$', s) is not None
