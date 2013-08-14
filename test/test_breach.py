import tutil
import unittest
import sys
import webvulnscan.attacks.breach
from webvulnscan.page import Page

try:
    from urllib.parse import unquote
except ImportError:
    from urllib2 import unquote


class BreachTest(unittest.TestCase):
    def test_static_site(self):
        default_page = Page("/", "<html></html>", {}, 200)

        class StaticSite(tutil.ClientSite):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                return default_page

        my_attack = webvulnscan.attacks.breach.BreachAttack(default_page)
        my_attack.run(StaticSite())

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "")

    def test_activated_gzip(self):
        default_page = Page("/", "<html></html>", {"Content-Encoding": "GZIP"},
                            200)

        class StaticSite(tutil.ClientSite):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                return default_page

        my_attack = webvulnscan.attacks.breach.BreachAttack(default_page)
        my_attack.run(StaticSite())

        output = sys.stdout.getvalue().strip()
        self.assertNotEqual(output, "")

    def test_breach_vulnerable(self):
        token = tutil.random_string(8)

        form = '<form action="/?a=b"><input name="text" type="text" />' \
               + '<input name="token" type="hidden" value="' + token \
               + '" /></form>'

        default_page = Page("/?a=b", "<html>" + form + "</html>",
                            {"Content-Encoding": "GZIP"}, 200)

        class StaticSite(tutil.ClientSite):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                return Page(url, "<html>" + form + unquote(url) + "</html>",
                            {"Content-Encoding": "GZIP"}, 200)

        my_attack = webvulnscan.attacks.breach.BreachAttack(default_page)
        my_attack.run(StaticSite())

        output = sys.stdout.getvalue().strip()
        self.assertNotEqual(output, "")
