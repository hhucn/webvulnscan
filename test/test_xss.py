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
    form = u'''<html><form action="./send" method="%s">
                    <input name="text" type="text" />
                </form></html>''' % method

    def xss_site(req):
        print(req.parameters)
        return u'<html>' + echo_param(req) + u'</html>'

    return {
        '/': form,
        '/send': xss_site,
    }


class XssTest(unittest.TestCase):
    @tutil.webtest({
        '/': u'''<html></html>''',
    }, [])
    def test_static_site(client):
        client.run_attack(webvulnscan.attacks.xss)

    @tutil.webtest(form_client('post',
                               lambda req: req.parameters['text']), ["XSS"])
    def test_xss_post_vulnerable_site(client):
        client.run_attack(webvulnscan.attacks.xss)

    @tutil.webtest(form_client('post',
                               lambda req: cgi.escape(req.parameters['text'])),
                   [])
    def test_xss_post_secure_site(client):
        client.run_attack(webvulnscan.attacks.xss)

    @tutil.webtest({
        '/': lambda req: u'<html>' + unquote(req.url) + '</html>',
    }, ["XSS"])
    def test_xss_url_vulnerable_site(client):
        client.run_attack(webvulnscan.attacks.xss, '?test=foo')

    @tutil.webtest({
        '/': lambda req: (u'<html>' +
                          cgi.escape(unquote(req.url)) + '</html>'),
    }, [])
    def test_xss_url_secure_site(client):
        client.run_attack(webvulnscan.attacks.xss)
