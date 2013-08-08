import unittest
import xml.etree.ElementTree as ET

import tutil
from webvulnscan.EtreeParser import EtreeParser


class EtreeParserTests(unittest.TestCase):
    def test_EtreeParser_valid(self):
        html = '<html><head>&uuml; &auml;</head></html>'
        parser = EtreeParser("http://example.site")
        ET.fromstring(html, parser)
