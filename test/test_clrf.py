import sys
import cgi
import tutil
import unittest

from webvulnscan.page import Page
import webvulnscan.attacks.clrf

try:
    from urllib.parse import unquote
except ImportError:
    from urllib2 import unquote


class ClrfAttackerTest(unittest.TestCase):
    def test_static_site(self):
        page = Page('/', '<html></html>', {}, 200)

        class StaticSite(object):
            def download_page(self, url, parameters=None):
                return page

        webvulnscan.attacks.clrf(page, StaticSite())

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "")

    def test_secured_url_site(self):
        page = Page('http://test/?random=test', '<html></html>', {}, 200)

        class SecuredUrlSite(object):
            def download_page(self, url, parameters=None):
                return Page('', "<html>" + cgi.escape(url) + "</html>",
                            {}, 200)

        webvulnscan.attacks.clrf(page, SecuredUrlSite())

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "")

    def test_secured_form_site(self):
        html = '<html><form action="/test"><input type="text" name="test">' \
               '</input></form></html>'
        page = Page('http://test/', html, {}, 200)

        class SecuredFormSite(object):
            def download_page(self, url, parameters={"test": "none"}):
                if not parameters["test"]:
                    parameters["test"] = ""

                return Page('', "<html>" + cgi.escape(parameters["test"]) +
                            "</html>", {}, 200)

        webvulnscan.attacks.clrf(page, SecuredFormSite())

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "")

    def test_secured_combo_site(self):
        html = '<html><form action="/test"><input type="text" name="test">' \
               '</input></form></html>'
        page = Page('http://test/?test=random', html, {}, 200)

        class SecuredComboSite(object):
            def download_page(self, url, parameters={"test": "none"}):
                if not parameters["test"]:
                    parameters["test"] = ""
                return Page('', "<html>" +
                            cgi.escape(parameters["test"] + url) + "</html>",
                            {}, 200)

        webvulnscan.attacks.clrf(page, SecuredComboSite())

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "")

    def test_vulnerable_url_site(self):
        page = Page('http://test/?random=test', '<html></html>', {}, 200)

        class VulnerableUrlSite(object):
            def download_page(self, url, parameters=None):
                _, _, url = url.partition('=')
                return Page('', unquote(url)[41:], {}, 200)

        webvulnscan.attacks.clrf(page, VulnerableUrlSite())

        output = sys.stdout.getvalue().strip()
        self.assertNotEqual(output, "")

    def test_vulnerable_form_site(self):
        html = '<html><form action="/test"><input type="text" name="test">' \
               '</input></form></html>'
        page = Page('http://test/', html, {}, 200)

        class VulnerableFormSite(object):
            def download_page(self, url, parameters={"test": "none"}):
                if not parameters["test"]:
                    parameters["test"] = ""

                return Page('', unquote(parameters["test"])[29:], {}, 200)

        webvulnscan.attacks.clrf(page, VulnerableFormSite())

        output = sys.stdout.getvalue().strip()
        self.assertNotEqual(output, "")
