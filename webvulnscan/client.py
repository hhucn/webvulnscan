import copy
import functools

from .compat import build_opener, HTTPCookieProcessor, URLError, \
    urlencode, CookieJar, HTTPError, BadStatusLine
from .utils import parse_content_type, NOT_A_PAGE_CONTENT_TYPES

import gzip
import zlib
import webvulnscan.log
from .page import Page
from .request import Request


class NotAPage(Exception):
    """ The content at the URL in question is not a webpage, but something
    static (image, text, etc.) """


class Client(object):
    """ Client provides a easy interface for accessing web content. """

    def __init__(self, log=webvulnscan.log):
        self.cookie_jar = CookieJar()
        self.opener = self.setup_opener()
        self.additional_headers = {}
        self.log = log

    def setup_opener(self):
        """ Builds the opener for the class. """
        cookie_handler = HTTPCookieProcessor(self.cookie_jar)
        opener = build_opener(cookie_handler)

        return opener

    def _download(self, request):
        self.log('info', request.url, "request", "Trying to request")
        try:
            response = self.opener.open(request)
        except HTTPError as error:
            response = error
        except URLError as error:
            if hasattr(self.log, 'warn'):
                self.log.warn(url, "unreachable")
            raise URLError(request.url + ' is unreachable: {0}'.format(error))
        except BadStatusLine as e:
            self.log('warn', request.url, 'Bad status line sent')
            return (request, 0, "", {})

        status_code = response.code
        headers = response.info()

        if headers.get('Content-Encoding') == "gzip":
            sim_file = gzip.GzipFile(fileobj=response)
            response_data = sim_file.read()
        elif headers.get('Content-Encoding') == "deflate":
            response_data = zlib.decompress(response.read())
        else:
            response_data = response.read()

        return (request, status_code, response_data, headers)

    def download(self, url_or_request, parameters=None, headers=None):
        """
        Downloads a URL, returns (request, status_code, response_data, headers)
        """

        if isinstance(url_or_request, Request):
            assert parameters is None
            assert headers is None
            request = url_or_request.copy()
        else:
            request = Request(url_or_request, parameters, headers)

        for header, value in self.additional_headers.items():
            request.add_header(header, value)

        msg = ('Requesting with parameters %s' % (request.parameters,)
               if request.parameters else
               'Requesting')
        self.log('info', request.url, 'client status', msg)

        return self._download(request)

    def download_page(self, url_or_request, parameters=None, req_headers=None):
        """ Downloads the content of a site, returns it as page.
        Throws NotAPage if the content is not a webpage.
        """

        request, status_code, html_bytes, headers = self.download(
            url_or_request, parameters, req_headers)

        content_type, charset = parse_content_type(
            headers.get('Content-Type'),
            logfunc=functools.partial(self.log, 'warn', request.url))

        if content_type in NOT_A_PAGE_CONTENT_TYPES:
            raise NotAPage()

        try:
            html = html_bytes.decode(charset, 'strict')
        except UnicodeDecodeError as ude:
            self.log('warn', request.url, 'Incorrect encoding', str(ude))
            html = html_bytes.decode(charset, 'replace')

        return Page(self.log, request, html, headers, status_code)
