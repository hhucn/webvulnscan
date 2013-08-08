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

from logging import getLogger

from .Page import Page

log = getLogger(__name__)

class StrangeContentType(Exception):
    def __init__(self):
        super(StrangeContentType, self).__init__()


class Client(object):
    def __init__(self):
        self.cookie_jar = CookieJar()
        self.opener = self.setup_opener() 
        self.visited_pages = []

    def setup_opener(self):
        redirect_handler = HTTPRedirectHandler()
        cookie_handler = HTTPCookieProcessor(self.cookie_jar)

        opener = build_opener(redirect_handler)
        opener = build_opener(cookie_handler)

        return opener


    def download(self, url, parameters=None, remember_visit=True):
        install_opener(self.opener)

        if parameters is None:
            request = Request(url)
        else:
            request = Request(url, parameters)

        status_code = 300

        try:
            response = self.opener.open(request)
        except HTTPError as error:
            status_code = error.code
        except URLError as error:
            log.exception("Can't reach " + url)
            raise

        headers = response.info()
        response_data = response.read()
        
        if remember_visit:
            self.visited_pages.append(url) 
        
        return status_code, response_data, headers

    def download_page(self, url, parameters=None, remember_visit=True):
        status_code, html, headers = self.download(url, parameters,
                                                   remember_visit)
        
        if "Content-Type" in headers:
            content_type, _, encoding = headers["Content-Type"].partition(";")

            if content_type == "text/html":
                # TODO encoding 
                html = html.decode("utf-8")
            else:
                raise StrangeContentType 

        else:
            log.warning("Warning no Content-Type header on" + url)
            html = html.decode("utf-8")

        return Page(url, html, headers, status_code)
