import unittest
import sys

import tutil
import webvulnscan.attacks.cookiescan


# A cookie is implicit cacheable, if
#  1. A cookie is set.
#  2. The Expire-Date is in the future
#  3. No Cache-Control is set.


def make_client(headers):
    headers['Content-Type'] = 'text/html; charset=utf-8'
    return tutil.TestClient({
        '/': (200, b'<html></html>', headers),
    })


class CookieScanTest(unittest.TestCase):
    def test_static_site(self):
        client = make_client({})
        client.run_attack(webvulnscan.attacks.cookiescan)
        client.log.assert_count(0)

    def test_insecure_site(self):
        client = make_client({
            "Set-Cookie": "random=test",
        })
        client.run_attack(webvulnscan.attacks.cookiescan)
        client.log.assert_count(1)

    def test_secure_site(self):
        client = make_client({
            "Set-Cookie": "random=test",
            "Cache-Control": "private",
        })
        client.run_attack(webvulnscan.attacks.cookiescan)
        client.log.assert_count(0)

    def test_secure_site_with_max_age(self):
        client = make_client({
            "Set-Cookie": "random=test",
            "Cache-Control": "max-age=0",
        })
        client.run_attack(webvulnscan.attacks.cookiescan)
        client.log.assert_count(0)
