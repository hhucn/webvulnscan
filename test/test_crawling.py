import unittest
import xml.etree.ElementTree

import tutil
import crawling


class CrawlingTest(unittest.TestCase):
    def test_crawl(self):
        doc = xml.etree.ElementTree.fromstring(
            '<html><a href="/x">link</a><a name="here">here</a></html>')
        self.assertEqual(list(crawling.links_on_site("http://test/", doc)),
                         ['http://test/x'])

    def test_from_crawl(self):
        doc = xml.etree.ElementTree.fromstring(
            '<html><form action="/x">'
            '<input type="text" name="test"></input>'
            '</form></html>')
        values = {x:y for x, y in crawling.forms_on_site("http://test", doc)}
        self.assertEqual(values, {"http://test/x": {"test": "text"}})

if __name__ == '__main__':
    unittest.main()
