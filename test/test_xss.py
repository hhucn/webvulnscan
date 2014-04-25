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
        return u'<html>' + echo_param(req) + u'</html>'

    return {
        '/': form,
        '/send': xss_site,
    }


class XssTest(unittest.TestCase):
    attack = webvulnscan.attacks.xss
    argument = '?test=foo'

    @tutil.webtest(False)
    def test_xss_static_site():
        return {
            '/': u'''<html></html>''',
        }

    @tutil.webtest(True)
    def test_xss_post_vulnerable_site():
        return form_client('post',
                           lambda req: req.parameters['text'])

    @tutil.webtest(False)
    def test_xss_post_secure_site():
        return form_client('post',
                           lambda req: cgi.escape(req.parameters['text']))

    @tutil.webtest(True)
    def test_xss_url_vulnerable_site():
        return form_client({
            '/': lambda req: u'<html>' + unquote(req.url) + '</html>',
        }, '?test=foo')

    @tutil.webtest(False)
    def test_xss_url_secure_site():
        return {
            '/': lambda req: (u'<html>' +
                              cgi.escape(unquote(req.url)) + '</html>'),
        }
