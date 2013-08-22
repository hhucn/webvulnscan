import unittest
from xml.etree.ElementTree import tostring

import tutil
from webvulnscan.html_parser import parse_html


class HTMLParserTests(unittest.TestCase):
    def test_valid(self):
        log = tutil.TestLog()
        html = u'<html><head>&uuml; &auml;</head></html>'
        parser = parse_html(html, "http://example.site", log=log)
        self.assertEqual(len(log.entries), 0)

    def test_forgot_close(self):
        log = tutil.TestLog()
        html = u'<html><body><theforgottentag>foo</body></html>'
        parse_html(html, "http://example.site", log=log)
        log.assertFound(u'Unclosed')
        log.assertFound(u'theforgottentag')
        self.assertEqual(len(log.entries), 1)

    def test_forgot_close_2(self):
        log = tutil.TestLog()
        html = u'<html><body><theforgottentag><alsonot>foo</body></html>'
        parse_html(html, "http://example.site", log=log)
        log.assertFound(u'Unclosed')
        log.assertFound(u'theforgottentag')
        log.assertFound(u'alsonot')
        self.assertEqual(len(log.entries), 2)

    def test_superflupus_close(self):
        log = tutil.TestLog()
        html = u'<html><body>foo</superfluous></body></html>'
        parse_html(html, "http://example html", log=log)
        log.assertFound(u'superfluous')
        self.assertEqual(len(log.entries), 1)

    def test_close_after_root(self):
        log = tutil.TestLog()
        html = u'<html><body>foo</body></html></superfluous>'
        parse_html(html, "http://example.site", log=log)
        log.assertFound(u'superfluous')
        log.assertFound(u'after root')
        self.assertEqual(len(log.entries), 1)

    def test_parse_empty(self):
        log = tutil.TestLog()
        html = u''
        doc = parse_html(html, "http://example.site", log=log)
        assert doc is not None
        self.assertEqual(len(log.entries), 1)

    def test_parse_textroot(self):
        log = tutil.TestLog()
        html = u'someText'
        parse_html(html, "http://example.site", log=log)
        log.assertFound(u'someText')
        self.assertTrue(len(log.entries) >= 1)

    def test_parse_text_before_root(self):
        log = tutil.TestLog()
        html = u'textBefore<b></b>'
        parse_html(html, "http://example.site", log=log)
        log.assertFound(u'Text')
        log.assertFound(u'textBefore')
        self.assertEqual(len(log.entries), 1)

    def test_parse_text_after_root(self):
        log = tutil.TestLog()
        html = u'<b/>c_textAfter'
        parse_html(html, "http://example.site", log=log)
        log.assertFound(u'Text')
        log.assertFound(u'textAfter')
        self.assertEqual(len(log.entries), 1)

    def test_fixup_forgotten_closing(self):
        log = tutil.TestLog()
        html = u'<html><body>go</body>'
        doc = parse_html(html, "http://example.site", log=log)
        self.assertEqual(tostring(doc), b'<html><body>go</body></html>')
        log.assertFound(u'html')
        self.assertEqual(len(log.entries), 1)

if __name__ == '__main__':
    unittest.main()
