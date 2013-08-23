from .compat import build_opener, Request, HTTPCookieProcessor, URLError, \
    urlencode, CookieJar, HTTPError

import gzip
import zlib
import webvulnscan.log
from .log import warn
from .page import Page


class NotAPage(Exception):
    """ The content at the URL in question is not a webpage, but something
    static (image, text, etc.) """


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


class Client(object):
    """ Client provides a easy interface for accessing web content. """

    def __init__(self):
        self.cookie_jar = CookieJar()
        self.opener = self.setup_opener()
        self.additional_headers = {"Content-Encoding": "gzip, deflate"}

    def setup_opener(self):
        """ Builds the opener for the class. """
        cookie_handler = HTTPCookieProcessor(self.cookie_jar)
        opener = build_opener(cookie_handler)

        return opener

    def download(self, url, parameters=None):
        """
        Downloads a site, returns (status_code, response_data, headers)
        """
        if parameters is None:
            request = Request(url)
        else:
            data = urlencode(parameters).encode("utf-8")
            request = Request(url, data)

        for header, value in self.additional_headers.items():
            request.add_header(header, value)

        if webvulnscan.log.very_verbose:
            if parameters:
                print("Requesting " + url + " with parameters " +
                      str(parameters))
            else:
                print("Requesting " + url)

        try:
            response = self.opener.open(request)
        except HTTPError as error:
            response = error
        except URLError as error:
            warn(url, "unreachable")
            raise

        status_code = response.code
        headers = response.info()

        if headers.get('Content-Encoding') == "gzip":
            sim_file = gzip.GzipFile(fileobj=response)
            response_data = sim_file.read()
        elif headers.get('Content-Encoding') == "deflate":
            response_data = zlib.decompress(response.read())
        else:
            response_data = response.read()

        return status_code, response_data, headers

    def download_page(self, url, parameters=None, blacklist=[]):
        """ Downloads the content of a site, returns it as page.
        Throws NotAPage if the content is not a webpage.
        """
        status_code, html_bytes, headers = self.download(url, parameters)
        if "Content-Type" in headers:
            content_type, _, encoding = headers["Content-Type"].partition(";")

            if content_type in NOT_A_PAGE_CONTENT_TYPES:
                raise NotAPage()
            elif content_type not in HTML_CONTENT_TYPES:
                warn(url, "Strange content type", content_type)

            attrib_name, _, charset = encoding.partition("=")
            if attrib_name.strip() != "charset":
                warn(url, "No Charset set")
                charset = 'utf-8'
        else:
            warn(url, "No Content-Type header, assuming text/html")
            charset = 'utf-8'

        try:
            html = html_bytes.decode(charset, 'strict')
        except UnicodeDecodeError as ude:
            warn(url, 'Incorrect encoding', str(ude))
            html = html_bytes.decode(charset, 'replace')

        return Page(url, html, headers, status_code, blacklist)
