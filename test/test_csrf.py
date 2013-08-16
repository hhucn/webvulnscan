import tutil
import sys
import unittest
import webvulnscan.attacks.csrf
from webvulnscan.page import Page


class CsrfTest(unittest.TestCase):
    def test_static_site(self):
        default_page = Page("/", "<html></html>", {}, 200)

        class StaticSite(tutil.ClientSite):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                return default_page

        webvulnscan.attacks.csrf(default_page, StaticSite())

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "")

    def test_csrf_protected_form(self):
        token = tutil.random_string(8)

        form = '<form action="/"><input name="text" type="text" />' \
               + '<input name="token" type="hidden" value="' + token \
               + '" /></form>'

        default_page = Page("/", "<html>" + form + "</html>", {}, 200)

        class ProtectedSite(tutil.ClientSite):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                if "token" in parameters:
                    if parameters["token"] == token:
                        return default_page

                return Page("/", "<html></html>", {}, 400)

        webvulnscan.attacks.csrf(default_page, ProtectedSite())

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "")

    def test_csrf_vulnerable(self):
        form = '<form action="/"><input name="text" type="text" /></form>'

        default_page = Page("/", "<html>" + form + "</html>", {}, 200)

        class VulnerableSite(tutil.ClientSite):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                return default_page

        webvulnscan.attacks.csrf(default_page, VulnerableSite())

        output = sys.stdout.getvalue().strip()
        self.assertNotEqual(output, "")
