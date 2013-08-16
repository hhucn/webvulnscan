import tutil
import unittest
import sys
import webvulnscan.attacks.cookiescan
from webvulnscan.page import Page

# A cookie is implicit cacheable, if
#  1. A cookie is set.
#  2. The Expire-Date is in the future
#  3. No Cache-Control is set.


class CookieScanTest(unittest.TestCase):
    def test_static_site(self):
        default_page = Page("/", "<html></html>",
                            {"Content-Type": "text/html"}, 200)

        class StaticSite(tutil.ClientSite):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                return default_page

        webvulnscan.attacks.cookiescan(default_page, StaticSite())

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "")

    def test_secure_site(self):
        default_page = Page("/", "<html></html>",
                            {"Content-Type": "text/html",
                             "Set-Cookie": "random=test",
                             "Cache-Control": "private"}, 200)

        class SecureSite(tutil.ClientSite):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                return default_page

        webvulnscan.attacks.cookiescan(default_page, SecureSite())

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "")

    def test_insecure_site(self):
        default_page = Page("/", "<html></html>",
                            {"Content-Type": "text/html",
                             "Set-Cookie": "random=test"}, 200)

        class InSecureSite(tutil.ClientSite):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                return default_page

        webvulnscan.attacks.cookiescan(default_page, InSecureSite())

        output = sys.stdout.getvalue().strip()
        self.assertNotEqual(output, "")
