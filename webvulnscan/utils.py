"""
Functions described here are for python 2/3 compability and other tasks.
"""

try:
    from urllib.parse import urlparse, parse_qsl, urlunparse, urlencode
except ImportError:
    from urlparse import urlparse, parse_qsl, urlunparse
    from urllib import urlencode


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
