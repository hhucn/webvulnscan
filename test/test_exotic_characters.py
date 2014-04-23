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
    @tutil.webtest({
        '/': u'''<html></html>''',
    }, [])
    def test_exotic_characters_static_site(client):
        client.run_attack(webvulnscan.attacks.exotic_characters)

    @tutil.webtest({
        '/': shell_emulation(lambda req: get_param(req.url, 'test')),
    }, SHELL_CHARACTERS)
    def test_exotic_characters_url_vulnerable_site(client):
        client.run_attack(webvulnscan.attacks.exotic_characters, u'?test=a')

    @tutil.webtest({
        '/': GENERIC_FORM,
        '/post': shell_emulation(lambda req: req.parameters['test']),
    }, SHELL_CHARACTERS)
    def test_exotic_characters_post_vulnerable_site(client):
        client.run_attack(webvulnscan.attacks.exotic_characters)

    @tutil.webtest({
        '/': GENERIC_FORM,
        '/post': u'<html>Properly escaped command</html>',
    }, [])
    def test_exotic_characters_valid_parsing(client):
        client.run_attack(webvulnscan.attacks.exotic_characters)
