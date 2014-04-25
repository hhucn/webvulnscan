import unittest
import xml.etree.ElementTree as ET

import tutil
import webvulnscan.page
import webvulnscan.request


def FakePage(html, headers={}, status_code=200, url="http://test/"):
    log = tutil.TestLog()
    req = webvulnscan.request.Request(url)
    return webvulnscan.page.Page(log, req, html=html,
                                 headers=headers, status_code=status_code)


class PageTest(unittest.TestCase):
    def test_generate_document(self):
        doc = '<html><a href="/x">link</a><a name="here">here</a></html>'
        parsed = ET.fromstring(doc)
        page = FakePage(doc)
        self.assertEqual(page.document.keys(), parsed.keys())
        self.assertEqual(page.document.items(), page.document.items())

    def test_get_links_no_links(self):
        doc = '<html>link</html>'
        page = FakePage(doc)
        output = set(page.get_links())
        self.assertEqual(output, set())

    def test_get_links_one_link(self):
        doc = '<html><a href="/test">click</a></html>'
        page = FakePage(doc)
        output = set(page.get_links())
        self.assertEqual(output, {"http://test/test"})

    def test_get_links_several(self):
        doc = '<html><a href="/1"></a><a href="/2"></a></html>'
        page = FakePage(doc)
        output = set(page.get_links())
        self.assertEqual(output, {"http://test/1", "http://test/2"})

    def test_get_url_parameters_none(self):
        doc = u'<html><a></a></html>'
        page = FakePage(doc)
        output = dict(page.url_parameters)
        self.assertEqual(output, dict())

    def test_get_url_parameters_one(self):
        doc = u'<html><a></a></html>'
        page = FakePage(doc, url=u'http://test/?test=1')
        output = dict(page.url_parameters)
        self.assertEqual(output, {'test': '1'})

    def test_get_url_parameters_several(self):
        doc = u'<html><a></a></html>'
        page = FakePage(doc, url=u'http://test/?test=1&other=2')
        output = dict(page.url_parameters)
        self.assertEqual(output, {'test': '1', 'other': '2'})

    def test_get_forms(self):
        html = u"<html><form action='/test'></form></html>"
        page = FakePage(html)
        self.assertNotEqual(list(page.get_forms()), None)

    def test_get_forms_blacklisted(self):
        html = u"<html><form action='/forbidden'></form></html>"
        blacklist = ["forbidden"]
        page = FakePage(html)
        self.assertEqual(list(page.get_forms(blacklist=blacklist)), [])

if __name__ == '__main__':
    unittest.main()
