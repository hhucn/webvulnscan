import unittest
import xml.etree.ElementTree as ET

import tutil
from webvulnscan.EtreeParser import EtreeParser


class EtreeParserTests(unittest.TestCase):
    def test_EtreeParser_valid(self):
        log = tutil.TestLog()
        html = '<html><head>&uuml; &auml;</head></html>'
        parser = EtreeParser("http://example.site", log=log)
        ET.fromstring(html, parser)
        self.assertEquals(len(log.entries), 0)

    def test_EtreeParse_forgot_close(self):
        log = tutil.TestLog()
        html = '<html><body><theforgottentag>foo</body></html>'
        parser = EtreeParser("http://example.site", log=log)
        ET.fromstring(html, parser)
        log.assertFound(u'Unclosed')
        log.assertFound(u'theforgottentag')
        self.assertEquals(len(log.entries), 1)

    def test_EtreeParse_forgot_close_2(self):
        log = tutil.TestLog()
        html = '<html><body><theforgottentag><alsonot>foo</body></html>'
        parser = EtreeParser("http://example.site", log=log)
        ET.fromstring(html, parser)
        log.assertFound(u'Unclosed')
        log.assertFound(u'theforgottentag')
        log.assertFound(u'alsonot')
        self.assertEquals(len(log.entries), 2)

    def test_EtreeParse_superflupus_close(self):
        log = tutil.TestLog()
        html = '<html><body>foo</superfluous></body></html>'
        parser = EtreeParser("http://example.site", log=log)
        ET.fromstring(html, parser)
        log.assertFound(u'superfluous')
        self.assertEquals(len(log.entries), 1)

    def test_EtreeParse_close_after_root(self):
        log = tutil.TestLog()
        html = '<html><body>foo</body></html></superfluous>'
        parser = EtreeParser("http://example.site", log=log)
        ET.fromstring(html, parser)
        log.assertFound(u'superfluous')
        log.assertFound(u'after root')
        self.assertEquals(len(log.entries), 1)


if __name__ == '__main__':
    unittest.main()
