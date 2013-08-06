import unittest
import xml.etree.ElementTree

import tutil
import webvulnscan


class CrawlingTest(unittest.TestCase):
    def test_crawl(self):
        doc = xml.etree.ElementTree.fromstring(
            '<html><a href="/x">link</a><a name="here">here</a></html>')
        self.assertEqual(list(webvulnscan.crawl(doc)), ['/x'])

    def test_from_crawl(self):
        doc = xml.etree.ElementTree.fromstring(
            '<html><form action="/x">'
            '<input type="text" name="test"></input>'
            '</form></html>')
        self.assertEqual(webvulnscan.form_crawl(doc),
                         {"/x": {"test": None}})

if __name__ == '__main__':
    unittest.main()
