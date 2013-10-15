import unittest
import cgi
import sys

import tutil
import webvulnscan.attacks.xss

try:
    from urllib.parse import unquote
except ImportError:
    from urllib2 import unquote


def form_client(method, echo_param):
    form = u'''<html><form action="/send" method="%s">
                    <input name="text" type="text" />
                </form></html>''' % method

    def xss_site(req):
        return u'<html>' + echo_param(req) + u'</html>'

    client = tutil.TestClient({
        '/': form,
        '/send': xss_site,
    })
    return client


class XssText(unittest.TestCase):
    def test_static_site(self):
        client = tutil.TestClient({
            '/': u'''<html></html>''',
        })
        client.run_attack(webvulnscan.attacks.xss)
        client.log.assert_count(0)

    def test_post_vulnerable_site(self):
        client = form_client('post', lambda req: req.parameters['text'])
        client.run_attack(webvulnscan.attacks.xss)
        client.log.assert_count(1)

    def test_post_secure_site(self):
        client = form_client('post',
                             lambda req: cgi.escape(req.parameters['text']))
        client.run_attack(webvulnscan.attacks.xss)
        client.log.assert_count(0)

    def test_url_vulnerable_site(self):
        client = tutil.TestClient({
            '/': lambda req: u'<html>' + unquote(req.url) + '</html>',
        })
        client.run_attack(webvulnscan.attacks.xss, '?test=foo')
        client.log.assert_count(1)

    def test_url_secure_site(self):
        client = tutil.TestClient({
            '/': lambda req: (u'<html>' +
                              cgi.escape(unquote(req.url)) + '</html>'),
        })
        client.run_attack(webvulnscan.attacks.xss)
        client.log.assert_count(0)
