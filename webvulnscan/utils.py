"""
Functions described here are for python 2/3 compability and other tasks.
"""

from .compat import (
    urlparse, urlencode, urljoin, parse_qsl, parse_qs)

import email.parser
import io
import json
import re
import sys

# Safe content types (will not be rendered as a webpage by the browser)
NOT_A_PAGE_CONTENT_TYPES = frozenset([
    'text/plain',
    'text/x-python',
    'image/gif',
    'image/jpeg',
    'image/png',
    'image/svg+xml',
])
HTML_CONTENT_TYPES = frozenset([
    "text/html",
    "application/xhtml+xml",
])


def parse_content_type(val, logfunc=None):
    if val:
        content_type, _, encoding = val.partition(";")

        if content_type in NOT_A_PAGE_CONTENT_TYPES:
            return (content_type, None)

        if content_type not in HTML_CONTENT_TYPES:
            if logfunc:
                logfunc(u'Strange content type', content_type)

        attrib_name, _, charset = encoding.partition('=')
        if attrib_name.strip() != "charset":
            if logfunc:
                logfunc(u'No Charset set')
            charset = 'utf-8'
    else:
        if logfunc:
            logfunc(u'No Content-Type header, assuming text/html')
        charset = 'utf-8'
        content_type = 'text/html'

    return (content_type, charset)


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
    return len(s) >= 6 and re.match(r'^[0-9a-fA-F$!]+$', s)


def get_param(url, pname):
    """ Return a GET parameter from a URL """
    return parse_qs(urlparse(url).query).get(pname, [u''])[0]


def add_get_params(url, params):
    assert isinstance(params, dict)

    for key in params.keys():
        params[key] = params[key].encode('ascii', 'ignore')

    return (url +
            (u'&' if u'?' in url else '?') +
            urlencode(params))


def parse_http_headers(bs):
    assert isinstance(bs, bytes)
    s = bs.decode('utf-8')
    p = email.parser.Parser()
    res = p.parse(io.StringIO(s), headersonly=True)
    return res
