import gzip
import io
import unittest

import tutil
import webvulnscan.attacks.breach
from webvulnscan.page import Page

try:
    from urllib.parse import unquote
except ImportError:
    from urllib2 import unquote


def _gzip_test_controller(html):
    def on_request(url, headers):
        content = html.encode('utf-8')
        out_headers = {'Content-Type': 'text/html; charset=utf-8'}
        if 'gzip' in headers.get('Acccept-Encoding', 'identity'):
            outs = io.BytesIO()
            with GZipFile(outs) as gf:
                gf.write(content)
            content = outs.getvalue()
            out_headers['Content-Encoding'] = 'gZiP'
        return (200, content)


class BreachTest(unittest.TestCase):
    def test_static_site(self):
        client = tutil.TestClient({
            '/': (200, b'<html></html>', {}),
        })
        webvulnscan.attacks.breach(client, client.log, client.ROOT_URL)
        self.assertEqual(len(client.log.entries), 0)

    def test_activated_gzip(self):
        client = tutil.TestClient({
            '/': _gzip_test_controller(u'<html></html>')
        })
        webvulnscan.attacks.breach(client, client.log, client.ROOT_URL)
        self.assertEqual(len(client.log.entries), 0)

    def test_no_token(self):
        token = "B0s3r W3rt"

        form = '<form action="/?a=b"><input name="text" type="text" />' \
               + '<input name="token" type="hidden" value="' + token \
               + '" /></form>'

        default_page = Page("/?a=b", "<html>" + form + "</html>",
                            {"Content-Encoding": "GZIP"}, 200)

        class VulnerableSite(tutil.ClientSite):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                return Page(url, "<html>" + form + unquote(url) + "</html>",
                            {"Content-Encoding": "GZIP"}, 200)

        webvulnscan.attacks.breach(default_page, VulnerableSite())

        output = sys.stdout.getvalue().strip()
        self.assertNotEqual(output, "")

    def test_not_reflected(self):
        token = tutil.random_string(8)

        form = '<form action="/?a=b"><input name="text" type="text" />' \
               + '<input name="token" type="hidden" value="' + token \
               + '" /></form>'

        default_page = Page("/?a=b", "<html>" + form + "</html>",
                            {"Content-Encoding": "GZIP"}, 200)

        class VulnerableSite(tutil.ClientSite):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                return Page(url, "<html></html>",
                            {"Content-Encoding": "GZIP"}, 200)

        webvulnscan.attacks.breach(default_page, VulnerableSite())

        output = sys.stdout.getvalue().strip()
        self.assertNotEqual(output, "")

    def test_breach_vulnerable(self):
        token = tutil.random_string(8)

        form = '<form action="/?a=b"><input name="text" type="text" />' \
               + '<input name="token" type="hidden" value="' + token \
               + '" /></form>'

        default_page = Page("/?a=b", "<html>" + form + "</html>",
                            {"Content-Encoding": "GZIP"}, 200)

        class VulnerableSite(tutil.ClientSite):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                return Page(url, "<html>" + form + unquote(url) + "</html>",
                            {"Content-Encoding": "GZIP"}, 200)

        webvulnscan.attacks.breach(default_page, VulnerableSite())

        output = sys.stdout.getvalue().strip()
        self.assertNotEqual(output, "")

if __name__ == '__main__':
    unittest.main()
