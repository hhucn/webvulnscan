import tutil
import unittest
import sys

import webvulnscan.attacks.broken_unicode_characters as broken_chars
from webvulnscan.page import Page

try:
    from urllib.parse import unquote
except ImportError:
    from urllib2 import unquote


class BrokenCharactersTest(unittest.TestCase):
    def test_static_site(self):
        default_page = Page("/", "<html></html>", {}, 200)

        class StaticSite(tutil.ClientSite):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                return default_page

        broken_chars(default_page, StaticSite())

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "")

    def test_url_vulnerable_site(self):
        default_page = Page("/?test=random", "<html></html>", {}, 200)

        class UrlVulnerableSite(tutil.ClientSite):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                url = unquote(str(url.encode('ascii', 'replace')))
                return Page("/", "<html>" + url.replace('>', '')
                            + "</html>", {}, 200)

        broken_chars(default_page, UrlVulnerableSite())

        output = sys.stdout.getvalue().strip()
        self.assertNotEqual(output, "")

    def test_post_vulnerable_site(self):
        default_page = Page("/?test",
                            '<html><form action="/test">'
                            '<input type="text" name="random" />'
                            '</form></html>', {}, 200)

        class FormVulnerableSite(tutil.ClientSite):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                if parameters["random"]:
                    item = parameters["random"].encode('ascii', 'replace')
                else:
                    item = "none"
                return Page("/", "<html>" + str(item) + "</html>", {}, 200)

        broken_chars(default_page, FormVulnerableSite())

        output = sys.stdout.getvalue().strip()
        self.assertNotEqual(output, "")

    def test_combo_vulnerable_site(self):
        default_page = Page("/?test=random",
                            '<html><form action="/test">'
                            '<input type="text" name="random" />'
                            '</form></html>', {}, 200)

        class ComboVulnerableSite(tutil.ClientSite):
            def download_page(self, url, parameters={"random": "none"},
                              remember_visited=None):
                if parameters["random"]:
                    item = parameters["random"].encode('ascii', 'ignore')
                else:
                    item = "none"
                return Page("/", "<html>" + item.decode() +
                            unquote(str(url)) + "</html>",
                            {}, 500)

        broken_chars(default_page, ComboVulnerableSite())

        output = sys.stdout.getvalue().strip()
        self.assertNotEqual(output, "")
