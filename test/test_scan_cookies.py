import unittest
import sys

import tutil
import webvulnscan.attacks.cookiescan


# A cookie is implicit cacheable, if
#  1. A cookie is set.
#  2. The Expire-Date is in the future
#  3. No Cache-Control is set.


def make_urlmap(headers):
    headers['Content-Type'] = 'text/html; charset=utf-8'
    return {
        '/': (200, b'<html></html>', headers),
    }


class CookieScanTest(unittest.TestCase):
    @tutil.webtest(make_urlmap({}), [])
    def test_cookie_static_site(client):
        client.run_attack(webvulnscan.attacks.cookiescan)

    @tutil.webtest(make_urlmap({
            "Set-Cookie": "random=test",
        }), ["Implicit cacheable cookie"])
    def test_cookie_insecure_site(client):
        client.run_attack(webvulnscan.attacks.cookiescan)

    @tutil.webtest(make_urlmap({
            "Set-Cookie": "random=test",
            "Cache-Control": "private",
        }), [])
    def test_cookie_secure_site(client):
        client.run_attack(webvulnscan.attacks.cookiescan)

    @tutil.webtest(make_urlmap({
            "Set-Cookie": "random=test",
            "Cache-Control": "max-age=0",
        }), [])
    def test_cookie_secure_site_with_max_age(client):
        client.run_attack(webvulnscan.attacks.cookiescan)
