from .utils import get_plain_text
from .EtreeParser import EtreeParser 
from logging import getLogger

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

try:
    from urllib.parse import parse_qsl
except ImportError:
    from urlparse import parse_qsl

from .Form import Form
import xml.etree.ElementTree as ET

log = getLogger(__name__)


class Page(object):
    """ Represents a page """
    def __init__(self, url, html, headers, status_code):
        """ Initalizes the Page object"""
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
            log.exception("Syntax error on Line " + str(error.position[0])
                          + " Column " + str(error.position[1]) + ":")
            log.exception(self.html.split('\n')[error.position[0]])
            raise

    def get_url_parameters(self):
        if "?" in self.url:
            url = self.url.split("?")[1]
        url_parts = parse_qsl(url)

        for parameter in url_parts:
            yield parameter[0], parameter[1]

    def get_forms(self):
        """ Generator for all forms on the page. """
        for form in self.document.findall('.//form[@action]'):
            yield Form(self.url, form)

    def get_links(self):
        """ Generator for all links on the page. """
        for link in self.document.findall('.//a[@href]'):
            href = link.attrib.get('href')
            yield urljoin(self.url, href)
