import tutil
import unittest
import random
import webvulnscan.attacks.breach
from webvulnscan.page import Page

try:
    from urllib.parse import unquote
except ImportError:
    from urllib2 import unquote


class BreachTest(unittest.TestCase):
    def test_static_site(self):
        default_page = Page("/", "<html></html>", {}, 300)

        class StaticSite(tutil.ClientSite):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                return default_page

        log_handler = tutil.LogHandler()
        my_attack = webvulnscan.attacks.breach.BreachAttack(default_page)
        my_attack.log = log_handler
        my_attack.run(StaticSite())

        self.assertEqual(len(log_handler.log_entrys), 0)

    def test_activated_gzip(self):
        default_page = Page("/", "<html></html>", {"Content-Encoding": "GZIP"},
                            300)

        class StaticSite(tutil.ClientSite):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                return default_page

        log_handler = tutil.LogHandler()
        my_attack = webvulnscan.attacks.breach.BreachAttack(default_page)
        my_attack.log = log_handler
        my_attack.run(StaticSite())

        self.assertEqual(len(log_handler.log_entrys), 1)

    def test_breach_vulnerable(self):
        token = [random.choice('01234567890ABCDEF') for x in range(8)]
        token = ''.join(token)

        form = '<form action="/?a=b"><input name="text" type="text" />' \
               + '<input name="token" type="hidden" value="' + token \
               + '" /></form>'

        default_page = Page("/?a=b", "<html>" + form + "</html>",
                            {"Content-Encoding": "GZIP"}, 300)

        class StaticSite(tutil.ClientSite):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                return Page(url, "<html>" + form + unquote(url) + "</html>",
                            {"Content-Encoding": "GZIP"}, 300)

        log_handler = tutil.LogHandler()
        my_attack = webvulnscan.attacks.breach.BreachAttack(default_page)
        my_attack.log = log_handler
        my_attack.run(StaticSite())

        self.assertEqual(len(log_handler.log_entrys), 1)
