import unittest
import xml.etree.ElementTree as ET

import tutil
import webvulnscan.page

class PageTest(unittest.TestCase):
    def test_generate_document(self):
        doc = '<html><a href="/x">link</a><a name="here">here</a></html>'
        parsed = ET.fromstring(doc)
        page = webvulnscan.page.Page("http://test/", doc, {}, 0)
        self.assertEqual(page.document.keys(), parsed.keys())
        self.assertEqual(page.document.items(), page.document.items())

    def test_get_links_no_links(self):
        doc = '<html>link</html>'
        page = webvulnscan.page.Page("http://test/", doc, {}, 0)
        output = tutil.gen_to_set(page.get_links())
        self.assertEqual(output, set())

    def test_get_links_one_link(self):
        doc = '<html><a href="/test">click</a></html>'
        page = webvulnscan.page.Page("http://test/", doc, {}, 0)
        output = tutil.gen_to_set(page.get_links())
        self.assertEqual(output, {"http://test/test"})

    def test_get_links_several(self):
        doc = '<html><a href="/1"></a><a href="/2"></a></html>'
        page = webvulnscan.page.Page("http://test/", doc, {}, 0)
        output = tutil.gen_to_set(page.get_links())
        self.assertEqual(output, {"http://test/1", "http://test/2"})

    def test_get_url_parameters_none(self):
        url = 'http://test/'
        page = webvulnscan.page.Page(url, '<a></a>', {}, 0)
        output = tutil.gen_to_set(page.get_links())
        self.assertEqual(output, set())

    def test_get_url_parameters_one(self):
        url = 'http://test/?test=1'
        page = webvulnscan.page.Page(url, '<a></a>', {}, 0)
        output = tutil.gen_to_set(page.get_links())
        self.assertEqual(output, {'test'})

    def test_get_url_parameters_several(self):
        url = 'http://test/?test=1&other=2'
        page = webvulnscan.page.Page(url, '<a></a>', {}, 0)
        output = tutil.gen_to_set(page.get_links())
        self.assertEqual(output, {'test', 'other'})

if __name__ == '__main__':
    unittest.main()
