import tutil
import unittest
import sys
import webvulnscan.attacks.clickjack
from webvulnscan.page import Page


class ClickjackTest(unittest.TestCase):
    def test_static_site(self):
        default_page = Page("/", "<html></html>",
                            {"Content-Type": "text/html"}, 200)

        class StaticSite(tutil.ClientSite):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                return default_page

        webvulnscan.attacks.clickjack(default_page, StaticSite())

        output = sys.stdout.getvalue().strip()
        self.assertNotEqual(output, "")

    def test_secured_site(self):
        default_page = Page("/", '<html><form action="somewhere">'
                            '</form></html>',
                            {'X-Frame-Options': 'DENY',
                             'Content-Type': 'text/html'}, 200)

        class SecuredSite(tutil.ClientSite):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                return default_page

        webvulnscan.attacks.clickjack(default_page, SecuredSite())

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "")

    def test_secured_site_with_link(self):
        default_page = Page("/", '<html><a href="/somesite?test"></a></html>',
                            {'X-Frame-Options': 'DENY',
                             'Content-Type': 'text/html'}, 200)

        class SecuredLinkSite(tutil.ClientSite):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                return default_page

        webvulnscan.attacks.clickjack(default_page, SecuredLinkSite())

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "")

    def test_sameorigin_site(self):
        default_page = Page("/", '<html><form action="somewhere">'
                            '</form></html>',
                            {'X-Frame-Options': 'SAME-ORIGIN',
                             'Content-Type': 'text/html'}, 200)

        class SameOriginSite(tutil.ClientSite):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                return default_page

        webvulnscan.attacks.clickjack(default_page, SameOriginSite())

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "")

    def test_sameorigin_link_site(self):
        default_page = Page("/", '<html><a href="/somesite?test"></a></html>',
                            {'X-Frame-Options': 'SAME-ORIGIN',
                             'Content-Type': 'text/html'}, 200)

        class SameOriginLinkSite(tutil.ClientSite):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                return default_page

        webvulnscan.attacks.clickjack(default_page, SameOriginLinkSite())

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "")

    def test_allowfrom_site(self):
        default_page = Page("/", '<html><form action="somewhere">'
                            '</form></html>',
                            {'X-Frame-Options': 'ALLOW-FROM http://test/',
                             'Content-Type': 'text/html'},
                            200)

        class AllowFromSite(tutil.ClientSite):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                return default_page

        webvulnscan.attacks.clickjack(default_page, AllowFromSite())

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "")

    def test_allowfrom_link_site(self):
        default_page = Page("/", '<html><a href="/somesite?test"></a></html>',
                            {'X-Frame-Options': 'ALLOW-FROM http://test/',
                             'Content-Type': 'text/html'},
                            200)

        class AllowFromLinkSite(tutil.ClientSite):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                return default_page

        webvulnscan.attacks.clickjack(default_page, AllowFromLinkSite())

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "")

    def test_vulnerable_site(self):
        default_page = Page("/", '<html><form action="somewhere">'
                            '</form></html>',
                            {'Content-Type': 'text/html'}, 200)

        class VulnerableSite(tutil.ClientSite):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                return default_page

        webvulnscan.attacks.clickjack(default_page, VulnerableSite())

        output = sys.stdout.getvalue().strip()
        self.assertNotEqual(output, "")

    def test_vulnerable_site_with_link(self):
        default_page = Page("/", '<html><a href="/somesite?test"></a></html>',
                            {'Content-Type': 'text/html'}, 200)

        class VulnerableLinkSite(tutil.ClientSite):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                return default_page

        webvulnscan.attacks.clickjack(default_page, VulnerableLinkSite())

        output = sys.stdout.getvalue().strip()
        self.assertNotEqual(output, "")
