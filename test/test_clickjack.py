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
    attack = webvulnscan.attacks.clickjack

    @tutil.webtest(False)
    def test_clickjack():
        return {
            '/': u'''<html>
                    <a href="./go">Links are (supposed to be) idempotent</a>
                    </html>'''
        }

    @tutil.webtest(False)
    def test_clickjack_get_form():
        return {
            '/': u'''<html>
                    <form>
                        The default method is GET, so this should be fine
                        <input type="submit" />
                    </form>
                    </html>'''
        }

    @tutil.webtest(False)
    def test_clickjack_get_form_second():
        return {
            '/': u'''<html>
                <form method="GET">
                    Explicitly specifying GET works too
                    <input type="submit" />
                </form>
                </html>'''
        }

    @tutil.webtest(True)
    def test_clickjack_vulnerable_site():
        return {
            '/': (
                200, FORM_HTML,
                {'Content-Type': 'text/html; charset=utf-8'}),
        }

    @tutil.webtest(True)
    def test_clickjack_vulnerable_alternative_content_type():
        return {
            '/': (
                200, FORM_HTML,
                {'Content-Type': 'application/xhtml+xml; charset=utf-8'}),
        }

    @tutil.webtest(False)
    def test_clickjack_secured_site():
        return {
            '/': (
                200, FORM_HTML,
                {'Content-Type': 'text/html; charset=utf-8',
            'X-Frame-Options': 'DENY'}),
        }

    @tutil.webtest(False)
    def test_clickjack_sameorigin_site():
        return {
            '/': (
                200, FORM_HTML,
                {'Content-Type': 'text/html; charset=utf-8',
                 'X-Frame-Options': 'SAMEORIGIN'}),
        }

    @tutil.webtest(False)
    def test_clickjack_allowfrom_site():
        return {
            '/': (
                200, FORM_HTML,
                {'Content-Type': 'text/html; charset=utf-8',
                 'X-Frame-Options': 'ALLOW-FROM http://safe.example.org/'}),
        }

    @tutil.webtest(True)
    def test_invalid_header():
        return {
            '/': (
                200, FORM_HTML,
                {'Content-Type': 'text/html; charset=utf-8',
                 'X-Frame-Options': 'None please!'}),
        }
