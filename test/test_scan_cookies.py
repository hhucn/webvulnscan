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
    attack = webvulnscan.attacks.cookiescan

    @tutil.webtest(False)
    def test_cookie_static_site():
        return make_urlmap({})

    @tutil.webtest(True)
    def test_cookie_insecure_site():
        return make_urlmap({
            "Set-Cookie": "random=test",
        })

    @tutil.webtest(False)
    def test_cookie_secure_site():
        return make_urlmap({
            "Set-Cookie": "random=test",
            "Cache-Control": "private",
        })

    @tutil.webtest(False)
    def test_cookie_secure_site_with_max_age():
        return make_urlmap({
            "Set-Cookie": "random=test",
            "Cache-Control": "max-age=0",
        })
