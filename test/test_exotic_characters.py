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
                <form action="./post" method="post">
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
    attack = webvulnscan.attacks.exotic_characters
    argument = '?test=a'

    @tutil.webtest(False)
    def test_exotic_characters_static_site():
        return {
            '/': u'''<html></html>''',
        }

    @tutil.webtest(True)
    def test_exotic_characters_url_vulnerable_site():
        return {
            '/': shell_emulation(lambda req: get_param(req.url, 'test')),
        }

    @tutil.webtest(True)
    def test_exotic_characters_post_vulnerable_site():
        return {
            '/': GENERIC_FORM,
            '/post': shell_emulation(lambda req: req.parameters['test']),
        }

    @tutil.webtest(False)
    def test_exotic_characters_valid_parsing():
        return {
            '/': GENERIC_FORM,
            '/post': u'<html>Properly escaped command</html>',
        }
