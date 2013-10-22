import unittest
from xml.etree.ElementTree import tostring

import tutil
from webvulnscan.html_parser import parse_html


class HTMLParserTests(unittest.TestCase):
    def test_valid(self):
        log = tutil.TestLog()
        html = u'<html><head>&uuml; &auml;</head></html>'
        parser = parse_html(html, "http://example.site", log=log)
        log.assert_count(0)

    def test_forgot_close(self):
        log = tutil.TestLog()
        html = u'<html><body><theforgottentag>foo</body></html>'
        parse_html(html, "http://example.site", log=log)
        log.assert_found(u'Unclosed')
        log.assert_found(u'theforgottentag')
        log.assert_count(1)

    def test_forgot_close_2(self):
        log = tutil.TestLog()
        html = u'<html><body><theforgottentag><alsonot>foo</body></html>'
        parse_html(html, "http://example.site", log=log)
        log.assert_found(u'Unclosed')
        log.assert_found(u'theforgottentag')
        log.assert_found(u'alsonot')
        log.assert_count(2)

    def test_superflupus_close(self):
        log = tutil.TestLog()
        html = u'<html><body>foo</superfluous></body></html>'
        parse_html(html, "http://example html", log=log)
        log.assert_found(u'superfluous')
        log.assert_count(1)

    def test_close_after_root(self):
        log = tutil.TestLog()
        html = u'<html><body>foo</body></html></superfluous>'
        parse_html(html, "http://example.site", log=log)
        log.assert_found(u'superfluous')
        log.assert_found(u'after root')
        log.assert_count(1)

    def test_parse_empty(self):
        log = tutil.TestLog()
        html = u''
        doc = parse_html(html, "http://example.site", log=log)
        assert doc is not None
        log.assert_count(1)

    def test_parse_textroot(self):
        log = tutil.TestLog()
        html = u'someText'
        parse_html(html, "http://example.site", log=log)
        log.assert_found(u'someText')
        self.assertTrue(len(log.entries) >= 1)

    def test_parse_text_before_root(self):
        log = tutil.TestLog()
        html = u'textBefore<b></b>'
        parse_html(html, "http://example.site", log=log)
        log.assert_found(u'Text')
        log.assert_found(u'textBefore')
        log.assert_count(1)

    def test_parse_text_after_root(self):
        log = tutil.TestLog()
        html = u'<b/>c_textAfter'
        parse_html(html, "http://example.site", log=log)
        log.assert_found(u'Text')
        log.assert_found(u'textAfter')
        log.assert_count(1)

    def test_parse_whitespace_before_root(self):
        log = tutil.TestLog()
        html = u' <b></b>'
        parse_html(html, "http://example.site", log=log)
        log.assert_count(0)

    def test_parse_whitespace_after_root(self):
        log = tutil.TestLog()
        html = u'<b/>\n\r\t'
        parse_html(html, "http://example.site", log=log)
        log.assert_count(0)

    def test_fixup_forgotten_closing(self):
        log = tutil.TestLog()
        html = u'<html><body>go</body>'
        doc = parse_html(html, "http://example.site", log=log)
        self.assertEqual(tostring(doc), b'<html><body>go</body></html>')
        log.assert_found(u'html')
        log.assert_count(1)

    def test_empty_tags(self):
        log = tutil.TestLog()
        html = u'<html><meta><body><input><br><img><hr></body></html>'
        doc = parse_html(html, "http://example.site", log=log)
        log.assert_count(0)

if __name__ == '__main__':
    unittest.main()
