try:
    from urllib.request import build_opener, Request, HTTPCookieProcessor, \
        URLError, HTTPError
except:
    from urllib2 import build_opener, Request, HTTPCookieProcessor, \
        URLError, HTTPError

try:
    from urllib.parse import urlencode, urljoin, parse_qsl, urlparse, \
        urlencode, quote_plus, parse_qs
except ImportError:
    from urlparse import urljoin, parse_qsl, parse_qs, urlparse
    from urllib import urlencode, quote_plus

try:
    from http.cookiejar import CookieJar, MozillaCookieJar
except ImportError:
    from cookielib import CookieJar, MozillaCookieJar

try:
    from html.parser import HTMLParser
except ImportError:  # Python < 3
    from HTMLParser import HTMLParser

try:
    from http.client import BadStatusLine
except ImportError:
    from httplib import BadStatusLine
