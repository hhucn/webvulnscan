import tutil
import unittest
import sys

import webvulnscan.log
import webvulnscan.attacks.breach
from webvulnscan.page import Page
from webvulnscan import print_logs

try:
    from urllib.parse import unquote
except ImportError:
    from urllib2 import unquote


class BreachTest(unittest.TestCase):
    def setUp(self):
        webvulnscan.log.do_print = True

    def test_static_site(self):
        default_page = Page("/", "<html></html>", {}, 200)

        class StaticSite(tutil.ClientSite):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                return default_page

        webvulnscan.attacks.breach(default_page, StaticSite())

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "")

    def test_activated_gzip(self):
        default_page = Page("/", "<html></html>", {"Content-Encoding": "GZIP"},
                            200)

        class GzippedSite(tutil.ClientSite):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                return default_page

        webvulnscan.attacks.breach(default_page, GzippedSite())
        print_logs()

        output = sys.stdout.getvalue().strip()
        self.assertNotEqual(output, "")

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
