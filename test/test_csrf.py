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

        my_attack = webvulnscan.attacks.csrf.CsrfAttack(default_page)
        my_attack.run(StaticSite())

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "")

    def test_csrf_protected_form(self):
        token = tutil.random_string(8)

        form = '<form action="/"><input name="text" type="text" />' \
               + '<input name="token" type="hidden" value="' + token \
               + '" /></form>'

        default_page = Page("/", "<html>" + form + "</html>", {}, 200)

        class StaticSite(tutil.ClientSite):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                if "token" in parameters:
                    if parameters["token"] == token:
                        return default_page

                return Page("/", "<html></html>", {}, 400)

        my_attack = webvulnscan.attacks.csrf.CsrfAttack(default_page)
        my_attack.client = StaticSite()
        my_attack.run()

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "")

    def test_csrf_vulnerable(self):
        form = '<form action="/"><input name="text" type="text" /></form>'

        default_page = Page("/", "<html>" + form + "</html>", {}, 200)

        class StaticSite(tutil.ClientSite):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                return default_page

        log_handler = tutil.LogHandler()
        my_attack = webvulnscan.attacks.csrf.CsrfAttack(default_page)
        my_attack.log = log_handler
        my_attack.run(StaticSite())

        output = sys.stdout.getvalue().strip()
        self.assertNotEqual(output, "")
