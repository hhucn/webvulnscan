""" Page.py module implements a page """
from .EtreeParser import EtreeParser
from .log import warn

from .compat import urljoin, parse_qsl

from .form import Form
from re import findall
import xml.etree.ElementTree as ET


class Page(object):
    def __init__(self, url, html, headers, status_code,  blacklist=[]):
        self.html = html
        self.headers = headers
        self.url = url
        self.status_code = status_code
        self.document = self.generate_document()

        self.blacklist = blacklist

    def generate_document(self):
        """ Generates the self.document attribute with a valid ElementTree. """
        parser = EtreeParser(self.url)
        try:
            return ET.fromstring(self.html, parser)
        except ET.ParseError as error:
            warn(self.url, "HTML Error", error.message)
            exit(2)

    @property
    def get_url_parameters(self):
        _, _, url = self.url.partition("?")
        return parse_qsl(url)

    def get_forms(self):
        """ Generator for all forms on the page. """
        for form in self.document.findall('.//form[@action]'):
            generated = Form(self.url, form)

            if any([findall(x, generated.action) for x in self.blacklist]):
                continue

            yield generated

    def get_links(self):
        """ Generator for all links on the page. """
        for link in self.document.findall('.//a[@href]'):
            href = link.attrib.get('href')
            yield urljoin(self.url, href)
