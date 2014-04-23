import sys
import unittest

import tutil
import webvulnscan

FORM_HTML = b'''<html>this is a form:
                <form action="./delete" method="post">
                    <input type="submit" />
                </form>
                </html>'''


class ClickjackTest(unittest.TestCase):
    @tutil.webtest({
            '/': u'''<html>
                <a href="./go">Links are (supposed to be) idempotent</a>
                </html>'''
        }, [])
    def test_static_site(client):
        client.run_attack(webvulnscan.attacks.clickjack)

    @tutil.webtest({
            '/': u'''<html>
                <form>
                    The default method is GET, so this should be fine
                    <input type="submit" />
                </form>
                </html>'''
        }, [])
    def test_clickjack_get_form(client):
        client.run_attack(webvulnscan.attacks.clickjack)

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

    @tutil.webtest({
            '/': (
                200, FORM_HTML,
                {'Content-Type': 'text/html; charset=utf-8'}),
        }, ["Clickjacking"])
    def test_clickjack_vulnerable_site(client):
        client.run_attack(webvulnscan.attacks.clickjack)

    @tutil.webtest({
            '/': (
                200, FORM_HTML,
                {'Content-Type': 'application/xhtml+xml; charset=utf-8'}),
        }, ["Clickjacking"])
    def test_clickjack_vulnerable_alternative_content_type(client):
        client.run_attack(webvulnscan.attacks.clickjack)

    @tutil.webtest({
            '/': (
                200, FORM_HTML,
                {'Content-Type': 'text/html; charset=utf-8',
                 'X-Frame-Options': 'DENY'}),
        }, [])
    def test_clickjack_secured_site(client):
        client.run_attack(webvulnscan.attacks.clickjack)

    @tutil.webtest({
            '/': (
                200, FORM_HTML,
                {'Content-Type': 'text/html; charset=utf-8',
                 'X-Frame-Options': 'SAMEORIGIN'}),
        }, [])
    def test_clickjack_sameorigin_site(client):
        client.run_attack(webvulnscan.attacks.clickjack)

    @tutil.webtest({
            '/': (
                200, FORM_HTML,
                {'Content-Type': 'text/html; charset=utf-8',
                 'X-Frame-Options': 'ALLOW-FROM http://safe.example.org/'}),
        }, [])
    def test_clickjack_allowfrom_site(client):
        client.run_attack(webvulnscan.attacks.clickjack)

    @tutil.webtest({
            '/': (
                200, FORM_HTML,
                {'Content-Type': 'text/html; charset=utf-8',
                 'X-Frame-Options': 'None please!'}),
        }, ["Clickjacking"])
    def test_invalid_header(client):
        client.run_attack(webvulnscan.attacks.clickjack)
