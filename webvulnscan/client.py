try:
    from http.cookiejar import CookieJar
except ImportError:
    from cookielib import CookieJar

try:
    from urllib.request import build_opener, install_opener, \
        HTTPRedirectHandler, Request, HTTPCookieProcessor, HTTPError, \
        URLError
except ImportError:
    from urllib2 import build_opener, install_opener, \
        HTTPRedirectHandler, Request, HTTPCookieProcessor, HTTPError, \
        URLError

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO

import gzip
from logging import getLogger

from .page import Page

log = getLogger(__name__)


class StrangeContentType(Exception):
    """ Thrown when Client isn't able to find something. """
    def __init__(self):
        super(StrangeContentType, self).__init__()


class Client(object):
    """ Client provides a easy interface for accessing web content. """
    def __init__(self):
        """ Initalises the class. """
        self.cookie_jar = CookieJar()
        self.opener = self.setup_opener()
        self.visited_pages = []
        self.additional_headers = {"Content-Encoding": "gzip, deflate"}

    def setup_opener(self):
        """ Builds the opener for the class. """
        redirect_handler = HTTPRedirectHandler()
        cookie_handler = HTTPCookieProcessor(self.cookie_jar)

        opener = build_opener(redirect_handler)
        opener = build_opener(cookie_handler)

        return opener

    def download(self, url, parameters=None, remember_visit=True):
        """ Downloads the content of a site, returns it as a string. """
        install_opener(self.opener)

        if parameters is None:
            request = Request(url)
        else:
            data = urlencode(parameters).encode("utf-8")
            request = Request(url, data)

        for header, value in self.additional_headers.items():
            request.add_header(header, value)

        try:
            response = self.opener.open(request)
        except HTTPError as error:
            response = error
        except URLError as error:
            log.exception("Can't reach " + url)
            raise

        status_code = response.code
        headers = dict(response.info().items())

        if "Content-Encoding" in headers:
            if headers["Content-Encoding"] == "gzip":
                io_buffer = StringIO(response.read())
                sim_file = gzip.GzipFile(fileobj=io_buffer)
                response_data = sim_file.read()
            else:
                response_data = response.read()
        else:
            response_data = response.read()

        if remember_visit:
            self.visited_pages.append(url)

        return status_code, response_data, headers

    def download_page(self, url, parameters=None, remember_visit=True):
        """ Downloads the content of a site, returns it as page. """
        status_code, html, headers = self.download(url, parameters,
                                                   remember_visit)
        if "Content-Type" in headers:
            content_type, _, encoding = headers["Content-Type"].partition(";")

            if content_type == "text/html":
                _, _, charset = encoding.partition("=")
                if charset == "":
                    log.warning("Warning no Charset set under " + url)
                    html = html.decode("utf-8")
                else:
                    html = html.decode(charset)

            else:
                raise StrangeContentType

        else:
            log.warning("Warning no Content-Type header on " + url)
            html = html.decode("utf-8")

        return Page(url, html, headers, status_code)
