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

__all__ = ['TestLog', 'TestClient', 'ContainsEverything']


# A little function for help.
def gen_to_set(generator):
    return {x for x in generator}


def gen_to_dict(generator):
    return {x: y for x, y in generator}


def random_token(length=8):
    return ''.join(random.choice(string.hexdigits) for _ in range(length))


LogEntry = collections.namedtuple('LogEntry', ['level', 'group', 'message'])


class TestLog(object):
    def __init__(self):
        self.entries = collections.deque()

    def log(self, entry):
        self.entries.append(entry)

    def warn(self, target, group, message=""):
        self.log(LogEntry('warn', group, message))

    def vulnerability(self, target, group, message=""):
        self.log(LogEntry('vuln', group, message))

    def assert_found(self, sub):
        assert any(sub in e.message for e in self.entries), (
            u'Expected to see "%s", but only got %r' % (
                (sub, [e.message for e in self.entries])))

    def assert_count(self, expected):
        assert len(self.entries) == expected, (
            u'Expected to see %d log entries, but got %d in log %r' %
            (expected, len(self.entries), list(self.entries)))


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
    , and whose values are tuples of (status_code, response_data, headers).

    For example, a valid url_map looks like:
    {
        u'http://localhost/': (200, b'<html/>', {}),
        u'/404': (404, b'Not found', {'Content-Type': 'text/html;'}),
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

    def download(self, url, parameters=None, headers=None):
        assert url in self.url_map
        res = self.url_map[url]
        if callable(res):
            headers = {}
            res = res(url, parameters, headers)
        return res

    def run_attack(self, attack):
        root_page = self.download_page(self.ROOT_URL)
        return attack(self, self.log, root_page)


class ContainsEverything(object):
    def __contains__(self, x):
        return True
