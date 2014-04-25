""" Common test setup functions """

import collections
import logging
import os.path
import string
import sys
import random


root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

# If this fails, we failed to set up the correct path above
import webvulnscan


def random_token(length=8):
    return ''.join(random.choice(string.hexdigits) for _ in range(length))


class TestLog(webvulnscan.log.Log):
    def assert_found(self, sub):
        assert any(sub in e.message for e in self.entries), (
            u'Expected to see "%s", but only got %r' % (
                (sub, [e.message for e in self.entries])))

    def assert_count(self, expected):
        assert len(self.entries) == expected, (
            u'Expected to see %d log entries, but got %d in log %r' %
            (expected, len(self.entries), list(self.entries)))

    def assert_vulnerable(self, vulnerable):
        was_vulnerable = len(self.entries) != 0
        assert was_vulnerable == vulnerable


# A class for writing site which are detemined
# to be request by webvulnscan.Client()
class ClientSite(object):
    def __init__(self):
        pass

    def download(self, url, parameters=None, remember_visited=None):
        pass

    def download_page(self, url, parameters=None, remember_visited=None):
        pass


class TestClient(webvulnscan.client.Client):
    """ url_map is a dict whose keys are either URLs or query strings,
    , and whose values are one of:
    * tuples of (status_code, response_data, headers)
    * just a unicode string
    * a callable returning a tuple or unicode string

    For example, a valid url_map looks like:
    {
        u'http://localhost/': (200, b'<html/>', {}),
        u'/404': (404, b'Not found', {'Content-Type': 'text/html;'}),
        u'/req': lambda request: u'<html/>',
    }
    """

    EXAMPLE_PREFIX = u'http://test.webvulnscan'

    def __init__(self, url_map, *args, **kwargs):
        super(TestClient, self).__init__(*args, log=TestLog(), **kwargs)
        self.url_map = dict(
            (self.full_url(url), content)
            for url, content in url_map.items()
        )

    @property
    def ROOT_URL(self):
        return self.EXAMPLE_PREFIX + u'/'

    def full_url(self, url):
        return url if u'://' in url else self.EXAMPLE_PREFIX + url

    def _download(self, req):
        req_url = req.url.partition(u'?')[0]
        assert req_url in self.url_map, u'Invalid request to %r' % req_url
        res = self.url_map[req_url]
        if callable(res):
            headers = {}
            res = res(req)
        if isinstance(res, type(u'')):
            status_code = 200
            response_data = res.encode('utf-8')
            headers = {'Content-Type': 'text/html; charset=utf-8'}
        else:
            status_code, response_data, headers = res

        assert isinstance(response_data, bytes), (
            u'Got invalid test response body %r' % (response_data,))
        return (req, status_code, response_data, headers)

    def run_attack(self, attack, add_url=u''):
        root_page = self.download_page(self.ROOT_URL + add_url)
        return attack(self, self.log, root_page)


def webtest(vulnerable):
    def wrapper(func):
        client = TestClient(func())
        argument = ""

        def res_func(self):
            if hasattr(self, "argument"):
                client.run_attack(self.attack, self.argument)
                argument = self.argument
            else:
                client.run_attack(self.attack)
            client.log.assert_vulnerable(vulnerable)

        res_func.__name__ = func.__name__
        res_func.client = client
        res_func.argument = argument

        return res_func

    return wrapper


class ContainsEverything(object):
    def __contains__(self, x):
        return True


def TokenController(value, method='post', field_name='token'):
    assert method in ('get', 'post')

    def on_request(request):
        parameters = request.parameters
        headers = request.headers
        url = request.url
        sent_value = parameters.get(field_name, u'')
        out_headers = {'Content-Type': 'text/html; charset=utf-8'}
        if value == sent_value:
            content = b'<html><body>Done.</body></html>'
            return (200, content, out_headers)
        else:
            content = b'<html><body>Wrong token.</body></html>'
            return (400, content, out_headers)
    return on_request


__all__ = ('TestLog', 'TestClient', 'TokenController', 'ContainsEverything')
