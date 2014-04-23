import sys
import unittest

import tutil
import webvulnscan.attacks.csrf
from webvulnscan.utils import get_param


def csrf_page(test_token):
    def sitef(req):
        if test_token(req):
            return u'<html>Thanks, posted</html>'
        else:
            return (
                400,
                b'<html>CSRF denied</html>',
                {'Content-Type': 'text/html; charset=utf-8'})
    return sitef

FORM_HTML = u'''<html>
    <form action="/s" method="post">
    <input name="text" type="text" />
    <input name="token" type="hidden" value="%s" />
    </form>
    </html>'''


def test_csrf_protected_form():
    token = tutil.random_token(8)
    return {
        '/': FORM_HTML % token,
        '/s': csrf_page(lambda req: get_param(req.url, 'text'))
    }


def test_csrf_vulnerable_form():
    token = tutil.random_token(8)
    return {
        '/': FORM_HTML % token,
        '/s': csrf_page(lambda req: True)
    }


class CsrfTest(unittest.TestCase):
    @tutil.webtest({
        '/': u'''<html></html>''',
    }, [])
    def test_static_site(client):
        client.run_attack(webvulnscan.attacks.csrf)

    @tutil.webtest(test_csrf_protected_form(), [])
    def test_csrf_protected_form(client):
        client.run_attack(webvulnscan.attacks.csrf)

    @tutil.webtest(test_csrf_vulnerable_form(), ["CSRF"])
    def test_csrf_vulnerable_post_form(client):
        client.run_attack(webvulnscan.attacks.csrf)
