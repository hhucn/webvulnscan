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


class CsrfTest(unittest.TestCase):
    def test_static_site(self):
        client = tutil.TestClient({
            '/': u'''<html></html>''',
        })
        client.run_attack(webvulnscan.attacks.csrf)
        client.log.assert_count(0)

    def test_csrf_protected_form(self):
        token = tutil.random_token(8)
        client = tutil.TestClient({
            '/': FORM_HTML % token,
            '/s': csrf_page(lambda req: get_param(req.url, 'text'))
        })
        client.run_attack(webvulnscan.attacks.csrf)
        client.log.assert_count(0)

    def test_csrf_vulnerable_post_form(self):
        token = tutil.random_token(8)
        client = tutil.TestClient({
            '/': FORM_HTML % token,
            '/s': csrf_page(lambda req: True)
        })
        client.run_attack(webvulnscan.attacks.csrf)
        client.log.assert_count(1)
