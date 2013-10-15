import sys
import unittest

import tutil
import webvulnscan

FORM_HTML = b'''<html>this is a form:
                <form action="/delete" method="post">
                    <input type="submit" />
                </form>
                </html>'''


class ClickjackTest(unittest.TestCase):
    def test_static_site(self):
        client = tutil.TestClient({
            '/': u'''<html>
                <a href="/go">Links are (supposed to be) idempotent</a>
                </html>'''
        })
        client.run_attack(webvulnscan.attacks.clickjack)
        client.log.assert_count(0)

    def test_get_form(self):
        client = tutil.TestClient({
            '/': u'''<html>
                <form>
                    The default method is GET, so this should be fine
                    <input type="submit" />
                </form>
                </html>'''
        })
        client.run_attack(webvulnscan.attacks.clickjack)
        client.log.assert_count(0)

        client = tutil.TestClient({
            '/': u'''<html>
                <form method="GET">
                    Explicitly specifying GET works too
                    <input type="submit" />
                </form>
                </html>'''
        })
        client.run_attack(webvulnscan.attacks.clickjack)
        client.log.assert_count(0)

    def test_vulnerable_site(self):
        client = tutil.TestClient({
            '/': (
                200, FORM_HTML,
                {'Content-Type': 'text/html; charset=utf-8'}),
        })
        client.run_attack(webvulnscan.attacks.clickjack)
        client.log.assert_count(1)

    def test_vulnerable_alternative_content_type(self):
        client = tutil.TestClient({
            '/': (
                200, FORM_HTML,
                {'Content-Type': 'application/xhtml+xml; charset=utf-8'}),
        })
        client.run_attack(webvulnscan.attacks.clickjack)
        client.log.assert_count(1)

    def test_secured_site(self):
        client = tutil.TestClient({
            '/': (
                200, FORM_HTML,
                {'Content-Type': 'text/html; charset=utf-8',
                 'X-Frame-Options': 'DENY'}),
        })
        client.run_attack(webvulnscan.attacks.clickjack)
        client.log.assert_count(0)

    def test_sameorigin_site(self):
        client = tutil.TestClient({
            '/': (
                200, FORM_HTML,
                {'Content-Type': 'text/html; charset=utf-8',
                 'X-Frame-Options': 'SAMEORIGIN'}),
        })
        client.run_attack(webvulnscan.attacks.clickjack)
        client.log.assert_count(0)

    def test_allowfrom_site(self):
        client = tutil.TestClient({
            '/': (
                200, FORM_HTML,
                {'Content-Type': 'text/html; charset=utf-8',
                 'X-Frame-Options': 'ALLOW-FROM http://safe.example.org/'}),
        })
        client.run_attack(webvulnscan.attacks.clickjack)
        client.log.assert_count(0)

    def test_invalid_header(self):
        client = tutil.TestClient({
            '/': (
                200, FORM_HTML,
                {'Content-Type': 'text/html; charset=utf-8',
                 'X-Frame-Options': 'None please!'}),
        })
        client.run_attack(webvulnscan.attacks.clickjack)
        client.log.assert_count(1)
