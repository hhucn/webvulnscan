import tutil
import unittest
import cgi
import sys

import webvulnscan.attacks.xss
from webvulnscan.page import Page

try:
    from urllib.parse import unquote
except ImportError:
    from urllib2 import unquote


class XssText(unittest.TestCase):
    def test_static_site(self):
        default_page = Page("/", "<html></html>", {}, 300)

        class StaticSite(tutil.ClientSite):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                return default_page

        webvulnscan.attacks.xss(default_page, StaticSite())

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "")

    def test_proctected_site(self):
        form = '<form action="/"><input name="text" type="text" /></form>'
        default_page = Page("/", "<html>" + form + "</html>", {}, 300)

        class ProtectedSite(tutil.ClientSite):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                first_parameter, value = parameters.popitem()
                html = "<html>" + form + cgi.escape(value) + "</html>"
                return Page("/", html, {}, 300)

        webvulnscan.attacks.xss(default_page, ProtectedSite())

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "")

    def test_url_vulnerable_site(self):
        default_page = Page("/test?random=get", "<html></html>",
                            {}, 200)

        class UrlVulnerableSite(tutil.ClientSite):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                html = "<html>" + unquote(url) + "</html>"
                return Page(url, html, {}, 200)

        webvulnscan.attacks.xss(default_page, UrlVulnerableSite())

        output = sys.stdout.getvalue().strip()
        self.assertNotEqual(output, "")

    def test_post_vulnerable_site(self):
        form = '<form action="/"><input name="text" type="text" /></form>'
        default_page = Page("/", "<html>" + form + "</html>", {}, 200)

        class PostVulnerableSite(tutil.ClientSite):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                first_parameter, value = parameters.popitem()
                html = "<html>" + form + value + "</html>"
                return Page("/", html, {}, 200)

        webvulnscan.attacks.xss(default_page, PostVulnerableSite())

        output = sys.stdout.getvalue().strip()
        self.assertNotEqual(output, "")

    def test_combo_vulnerable_site(self):
        form = '<form action="/?value=test">' \
               + '<input name="text" type="text" /></form>'

        default_page = Page("/?value=test", "<html>" + form + "</html>", {},
                            300)

        class ComboVulnerableSite(tutil.ClientSite):
            def download_page(self, url, parameters={"value": "test"},
                              remember_visited=None):
                first_parameter, value = parameters.popitem()
                html = "<html>" + form + value + unquote(url) + "</html>"
                return Page(url, html, {}, 300)

        webvulnscan.attacks.xss(default_page, ComboVulnerableSite())

        output = sys.stdout.getvalue().strip()
        self.assertNotEqual(output, "")
