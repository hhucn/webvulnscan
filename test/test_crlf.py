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
        html = (u'<html>%s</html>' % cgi.escape(p)).encode('utf-8')
        header_bytes = b'\r\n'.join([
            b'Content-Type: text/html; charset=utf-8',
            b'Set-Cookie: url=' + encode(p)
        ])
        headers = parse_http_headers(header_bytes)
        return (200, html, headers)
    return site


class CRLFAttackerTest(unittest.TestCase):
    @tutil.webtest({
        '/': lambda req: u'<html>%s</html>' % cgi.escape(req.url),
    }, [])
    def test_clrf_static_site(client):
        client.run_attack(webvulnscan.attacks.crlf)

    @tutil.webtest({
        '/': header_site(lambda req: get_param(req.url, 'foo'), True)
    }, ["CLRF"])
    def test_clrf_vulnerable_url_site(client):
        client.run_attack(webvulnscan.attacks.crlf, u'?foo=bar')

    @tutil.webtest({
        '/': header_site(lambda req: get_param(req.url, 'foo'), False)
    }, [])
    def test_clrf_secure_url_site(client):
        client.run_attack(webvulnscan.attacks.crlf, u'?foo=bar')

    @tutil.webtest({
        '/': u'''<html><form method="post" action="./post">
                 <input name="foo" /></form></html>''',
        '/post': header_site(lambda req: req.parameters.get('foo'), True)
    }, ["CLRF"])
    def test_clrf_vulnerable_post_site(client):
        client.run_attack(webvulnscan.attacks.crlf)

    @tutil.webtest({
        '/': u'''<html><form method="post" action="./post">
                 <input name="foo" /></form></html>''',
        '/post': header_site(lambda req: req.parameters.get('foo'), False)
    }, [])
    def test_clrf_secure_post_site(client):
        client.run_attack(webvulnscan.attacks.crlf)

    @tutil.webtest({
        '/': u'''<html><form action="./post">
                 <input name="foo" /></form></html>''',
        '/post': header_site(lambda req: get_param(req.url, 'foo'), True)
    }, ["CLRF"])
    def test_clrf_vulnerable_get_site(client):
        client.run_attack(webvulnscan.attacks.crlf)

    @tutil.webtest({
        '/': u'''<html><form action="./post">
                 <input name="foo" /></form></html>''',
        '/post': header_site(lambda req: get_param(req.url, 'foo'), False)
    }, [])
    def test_clrf_secure_get_site(client):
        client.run_attack(webvulnscan.attacks.crlf)
