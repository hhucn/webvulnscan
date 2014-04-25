import base64
import cgi
import tutil
import unittest

from webvulnscan.page import Page
from webvulnscan.utils import get_param, parse_http_headers
import webvulnscan.attacks.crlf

try:
    from urllib.parse import unquote
except ImportError:
    from urllib2 import unquote


def header_site(getparam, vulnerable):
    if vulnerable:
        encode = lambda s: s.encode('utf-8')
    else:
        # There is no defined encoding in practice, so let's just base64
        # all user input
        encode = lambda s: base64.b64encode(s.encode('utf-8'))

    def site(req):
        p = getparam(req)
        if p is None:
            p = ""
        html = (u'<html>%s</html>' % cgi.escape(p)).encode('utf-8')
        header_bytes = b'\r\n'.join([
            b'Content-Type: text/html; charset=utf-8',
            b'Set-Cookie: url=' + encode(p)
        ])
        headers = parse_http_headers(header_bytes)
        parsed_headers = {}
        for value, key in headers.items():
            parsed_headers[value] = key
        return (200, html, parsed_headers)
    return site


class CRLFAttackerTest(unittest.TestCase):
    attack = webvulnscan.attacks.crlf
    argument = "?foo=bar"

    @tutil.webtest(False)
    def test_clrf_static_site():
        return {
            '/': lambda req: u'<html>%s</html>' % cgi.escape(req.url),
        }

    @tutil.webtest(True)
    def test_clrf_vulnerable_url_site():
        return {
            '/': header_site(lambda req: get_param(req.url, 'foo'), True)
        }

    @tutil.webtest(False)
    def test_clrf_secure_url_site():
        return {
            '/': header_site(lambda req: get_param(req.url, 'foo'), False)
        }

    @tutil.webtest(True)
    def test_clrf_vulnerable_post_site():
        return {
            '/': u'''<html><form method="post" action="./post">
                     <input name="foo" /></form></html>''',
            '/post': header_site(lambda req: req.parameters.get('foo'), True)
        }

    @tutil.webtest(False)
    def test_clrf_secure_post_site():
        return {
            '/': u'''<html><form method="post" action="./post">
                     <input name="foo" /></form></html>''',
            '/post': header_site(lambda req: req.parameters.get('foo'), False)
        }

    @tutil.webtest(True)
    def test_clrf_vulnerable_get_site():
        return {
            '/': u'''<html><form action="./post">
                     <input name="foo" /></form></html>''',
            '/post': header_site(lambda req: get_param(req.url, 'foo'), True)
        }

    @tutil.webtest(False)
    def test_clrf_secure_get_site():
        return {
            '/': u'''<html><form action="./post">
                     <input name="foo" /></form></html>''',
            '/post': header_site(lambda req: get_param(req.url, 'foo'), False)
        }
