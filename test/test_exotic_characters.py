import tutil
import unittest
import sys

import webvulnscan.attacks.exotic_characters
from webvulnscan.utils import get_param

try:
    from urllib.parse import unquote
except ImportError:
    from urllib2 import unquote


SHELL_CHARACTERS = u'"\'|;<>\0'
GENERIC_FORM = u'''<html>
                <form action="/post" method="post">
                <input type="text" name="test" />
                </form>
                </html>'''


def shell_emulation(getinput):
    def site(req):
        s = getinput(req)
        # A real application would run subprocess.Popen(..., shell=True) or so
        if any(c in s for c in SHELL_CHARACTERS):
            return (
                500,
                b'<html>Syntax Error</html>',
                {'Content-Type': 'text/html; charset=utf-8'}
            )
        return u'<html>Process executed.</html>'
    return site


class ExoticCharacterTest(unittest.TestCase):
    def test_static_site(self):
        client = tutil.TestClient({
            '/': u'''<html></html>''',
        })
        client.run_attack(webvulnscan.attacks.exotic_characters)
        client.log.assert_count(0)

    def test_url_vulnerable_site(self):
        client = tutil.TestClient({
            '/': shell_emulation(lambda req: get_param(req.url, 'test')),
        })
        client.run_attack(webvulnscan.attacks.exotic_characters, u'?test=a')
        client.log.assert_count(len(SHELL_CHARACTERS))

    def test_post_vulnerable_site(self):
        client = tutil.TestClient({
            '/': GENERIC_FORM,
            '/post': shell_emulation(lambda req: req.parameters['test']),
        })
        client.run_attack(webvulnscan.attacks.exotic_characters)
        client.log.assert_count(len(SHELL_CHARACTERS))

    def test_valid_parsing(self):
        client = tutil.TestClient({
            '/': GENERIC_FORM,
            '/post': u'<html>Properly escaped command</html>',
        })
        client.run_attack(webvulnscan.attacks.exotic_characters)
        client.log.assert_count(0)
