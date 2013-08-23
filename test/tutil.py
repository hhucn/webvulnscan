""" Common test setup functions """

import collections
import logging
import os.path
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


# Random String generator for tokens, etc...
def random_string(length):
    return ''.join([random.choice('01234567890ABCDEF') for x in range(8)])


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

    def assertFound(self, sub):
        assert any(sub in e.message for e in self.entries), (
            u'Expected to see "%s", but only got %r' % (
                (sub, [e.message for e in self.entries])))


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

    def download(self, url, parameters=None):
        assert url in self.url_map
        return self.url_map[url]


class ContainsEverything(object):
    def __contains__(self, x):
        return True
