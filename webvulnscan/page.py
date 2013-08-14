""" Page.py module implements a page """
from .EtreeParser import EtreeParser
from logging import getLogger

from .compat import urljoin, parse_qsl

from .form import Form
import xml.etree.ElementTree as ET

log = getLogger(__name__)


class Page(object):
    def __init__(self, url, html, headers, status_code):
        self.html = html
        self.headers = headers
        self.url = url
        self.status_code = status_code
        self.document = self.generate_document()

    def generate_document(self):
        """ Generates the self.document attribute with a valid ElementTree. """
        parser = EtreeParser(self.url)
        try:
            return ET.fromstring(self.html, parser)
        except ET.ParseError as error:
            print("Syntax error on Line " + str(error.position[0])
                  + " Column " + str(error.position[1]) + ":")
            print(self.html.split('\n')[error.position[0]])
            raise

    @property
    def get_url_parameters(self):
        _, _, url = self.url.partition("?")
        return parse_qsl(url)

    def get_forms(self):
        """ Generator for all forms on the page. """
        for form in self.document.findall('.//form[@action]'):
            yield Form(self.url, form)

    def get_links(self):
        """ Generator for all links on the page. """
        for link in self.document.findall('.//a[@href]'):
            href = link.attrib.get('href')
            yield urljoin(self.url, href)
