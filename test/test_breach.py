import gzip
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


class BreachTest(unittest.TestCase):
    def test_static_site(self):
        client = tutil.TestClient({
            '/': u'<html></html>',
        })
        client.run_attack(webvulnscan.attacks.breach)
        client.log.assert_count(0)

    def test_activated_gzip(self):
        client = tutil.TestClient({
            '/': _gzip_test_controller(u'<html></html>')
        })
        client.run_attack(webvulnscan.attacks.breach)
        client.log.assert_count(0)

    def test_no_token(self):
        html = u'''
<html>
<body>
<form action="/search" method="POST">
  <input name="text" type="text" />
  <input name="username" type="hidden" value="B0s3r W3rt" />
  <input name="msgid" type="hidden" value="43" />
</form>
</body>
</html>
'''
        client = tutil.TestClient({
            '/': _gzip_test_controller(html),
            '/seach': (
                200,
                b'<html>Here are your results</html>',
                {'Content-Type': 'text/html; charset=utf-8'}),
        })
        client.run_attack(webvulnscan.attacks.breach)
        client.log.assert_count(0)

    def test_breach_vulnerable(self):
        token = tutil.random_token(16)
        html = u'''
<html>
<body>
<form action="/post" method="post">
  <input name="text" type="text" />
  <input name="token" type="hidden" value="%s" />
</form>
</body>
</html>
''' % token
        client = tutil.TestClient({
            '/': _gzip_test_controller(html),
            '/post': tutil.TokenController(token),
        })
        client.run_attack(webvulnscan.attacks.breach)
        client.log.assert_count(1)

    @unittest.skip('Not yet supported')
    def test_breach_vulnerable_urltoken(self):
        token = tutil.random_token(16)
        html = u'''
<html>
<body>
<form action="/post?token=%s" method="post">
  <input name="text" type="text" />
</form>
</body>
</html>
''' % token
        client = tutil.TestClient({
            '/': _gzip_test_controller(html),
            '/post': tutil.TokenController(token, method='get')
        })
        client.run_attack(webvulnscan.attacks.breach)
        client.log.assert_count(1)


if __name__ == '__main__':
    unittest.main()
