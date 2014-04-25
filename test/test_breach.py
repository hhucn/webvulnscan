import gzip
import zlib
import io
import unittest

import tutil
import webvulnscan.attacks.breach
from webvulnscan.page import Page


try:
    from urllib.parse import unquote
except ImportError:
    from urllib2 import unquote


def _gzip_test_controller(html):
    def on_request(request):
        content = html.encode('utf-8')
        out_headers = {'Content-Type': 'text/html; charset=utf-8'}
        if 'gzip' in request.headers.get('Acccept-Encoding', 'identity'):
            outs = io.BytesIO()
            with GZipFile(outs) as gf:
                gf.write(content)
            content = outs.getvalue()
            out_headers['Content-Encoding'] = 'gZiP'
        return (200, content, out_headers)
    return on_request


def _deflate_test_controller(html):
    def on_request(request):
        content = html.encode('utf-8')
        out_headers = {'Content-Type': 'text/html; charset=utf-8'}
        if 'deflate' in request.headers.get('Acccept-Encoding', 'identity'):
            content = zlib.compress(content)
            out_headers['Content-Encoding'] = 'deflate'
        return (200, content, out_headers)
    return on_request


def _breach_vulnerable():
    token = tutil.random_token(16)
    return {
        '/': _gzip_test_controller(u'''
<html>
<body>
<form action="./post" method="post">
  <input name="text" type="text" />
  <input name="token" type="hidden" value="%s" />
</form>
</body>
</html>
''' % token),
        '/post': tutil.TokenController(token)
    }


class BreachTest(unittest.TestCase):
    attack = webvulnscan.attacks.breach

    @tutil.webtest(False)
    def test_breach_static_site():
        return {'/': u'<html></html>'}

    @tutil.webtest(False)
    def test_activated_gzip():
        return {
            '/': _gzip_test_controller(u'<html></html>')
        }

    @tutil.webtest(False)
    def test_no_token():
        return {'/': _gzip_test_controller(u'''
<html>
<body>
<form action="./search" method="POST">
  <input name="text" type="text" />
  <input name="username" type="hidden" value="B0s3r W3rt" />
  <input name="msgid" type="hidden" value="43" />
</form>
</body>
</html>
'''),
                '/search': (
                    200,
                    b'<html>Here are your results</html>',
                    {'Content-Type': 'text/html; charset=utf-8'})}

    @tutil.webtest(True)
    def test_breach_vulnerable():
        return _breach_vulnerable()

    @unittest.skip('Not yet supported')
    def test_breach_vulnerable_urltoken():
        token = tutil.random_token(16)
        html = u'''
<html>
<body>
<form action="./post?token=%s" method="post">
  <input name="text" type="text" />
</form>
</body>
</html>
''' % token
        client = tutil.TestClient({
            '/': _gzip_test_controller(html),
            '/post': tutil.TokenController(token, method='get')
        })
        client.log.assert_count(1)

    @tutil.webtest(False)
    def test_activated_deflate():
        return {'/': _deflate_test_controller(u'<html></html>')}

    @tutil.webtest(False)
    def test_no_token_with_deflate():
        html = u'''
<html>
<body>
<form action="./search" method="POST">
  <input name="text" type="text" />
  <input name="username" type="hidden" value="B0s3r W3rt" />
  <input name="msgid" type="hidden" value="43" />
</form>
</body>
</html>
'''
        return {
            '/': _deflate_test_controller(html),
            '/search': (
                200,
                b'<html>Here are your results</html>',
                {'Content-Type': 'text/html; charset=utf-8'})
        }

    @tutil.webtest(True)
    def test_breach_vulnerable_with_deflate():
        token = tutil.random_token(16)
        html = u'''
<html>
<body>
<form action="./post" method="post">
  <input name="text" type="text" />
  <input name="token" type="hidden" value="%s" />
</form>
</body>
</html>
''' % token
        return {
            '/': _deflate_test_controller(html),
            '/post': tutil.TokenController(token),
        }

    @unittest.skip('Not yet supported')
    def test_breach_vulnerable_urltoken_with_deflate():
        token = tutil.random_token(16)
        html = u'''
<html>
<body>
<form action="./post?token=%s" method="post">
  <input name="text" type="text" />
</form>
</body>
</html>
''' % token
        client = tutil.TestClient({
            '/': _deflate_test_controller(html),
            '/post': tutil.TokenController(token, method='get')
        })
        client.log.assert_count(1)

if __name__ == '__main__':
    unittest.main()
