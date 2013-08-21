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

__all__ = ['TestLog']


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
