""" Page.py module implements a page """
from .html_parser import parse_html

from .compat import urljoin, parse_qsl

from .form import Form
from re import search


class Page(object):
    def __init__(self, log, request, html, headers, status_code):
        assert hasattr(request, 'url')
        self.request = request
        self.html = html
        self.headers = headers
        self.status_code = status_code
        self.document = parse_html(html, request.url, log)

    @property
    def url(self):
        return self.request.url

    @property
    def url_parameters(self):
        _, _, url = self.url.partition("?")
        return parse_qsl(url)

    def get_forms(self, blacklist=[]):
        """ Generator for all forms on the page. """
        for form in self.document.findall('.//form'):
            generated = Form(self.url, form)

            if any(search(x, generated.action) for x in blacklist):
                continue

            yield generated

    def get_links(self, blacklist=[]):
        """ Generator for all links on the page. """
        for link in self.document.findall('.//a[@href]'):
            href = link.attrib.get('href')
            url = urljoin(self.url, href)
            if any(search(x, url) for x in blacklist):
                continue
            yield url
