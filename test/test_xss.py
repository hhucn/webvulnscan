import tutil
import unittest
import cgi
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

        log_handler = tutil.LogHandler()
        my_attack = webvulnscan.attacks.xss.XssAttack(default_page)
        my_attack.log = log_handler
        my_attack.client = StaticSite()
        my_attack.run()

        self.assertEqual(len(log_handler.log_entrys), 0)

    def test_proctected_site(self):
        form = '<form action="/"><input name="text" type="text" /></form>'

        default_page = Page("/", "<html>" + form + "</html>", {}, 300)

        class StaticSite(tutil.ClientSite):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                first_parameter, value = parameters.popitem()
                html = "<html>" + form + cgi.escape(value) + "</html>"
                return Page("/", html, {}, 300)

        log_handler = tutil.LogHandler()
        my_attack = webvulnscan.attacks.xss.XssAttack(default_page)
        my_attack.log = log_handler
        my_attack.client = StaticSite()
        my_attack.run()

        self.assertEqual(len(log_handler.log_entrys), 0)

    def test_url_vulnerable_site(self):
        default_page = Page("/test?random=get", "<html></html>",
                            {}, 300)

        class StaticSite(tutil.ClientSite):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                html = "<html>" + unquote(url) + "</html>"
                return Page(url, html, {}, 300)

        log_handler = tutil.LogHandler()
        my_attack = webvulnscan.attacks.xss.XssAttack(default_page)
        my_attack.log = log_handler
        my_attack.client = StaticSite()
        my_attack.run()

        self.assertEqual(len(log_handler.log_entrys), 1)

    def test_post_vulnerable_site(self):
        form = '<form action="/"><input name="text" type="text" /></form>'

        default_page = Page("/", "<html>" + form + "</html>", {}, 300)

        class StaticSite(tutil.ClientSite):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                first_parameter, value = parameters.popitem()
                html = "<html>" + form + value + "</html>"
                return Page("/", html, {}, 300)

        log_handler = tutil.LogHandler()
        my_attack = webvulnscan.attacks.xss.XssAttack(default_page)
        my_attack.log = log_handler
        my_attack.client = StaticSite()
        my_attack.run()

        self.assertEqual(len(log_handler.log_entrys), 1)

    def test_combo_vulnerable_site(self):
        form = '<form action="/?value=test">' \
               + '<input name="text" type="text" /></form>'

        default_page = Page("/?value=test", "<html>" + form + "</html>", {},
                            300)

        class StaticSite(tutil.ClientSite):
            def download_page(self, url, parameters={"value": "test"},
                              remember_visited=None):
                first_parameter, value = parameters.popitem()
                print(value)
                html = "<html>" + form + value + unquote(url) + "</html>"
                return Page(url, html, {}, 300)

        log_handler = tutil.LogHandler()
        my_attack = webvulnscan.attacks.xss.XssAttack(default_page)
        my_attack.log = log_handler
        my_attack.client = StaticSite()
        my_attack.run()

        print(log_handler.log_entrys)
        self.assertEqual(len(log_handler.log_entrys), 2)
