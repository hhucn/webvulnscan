""" Common test setup functions """

import logging
import os.path
import sys
import random


root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

# If this fails, we failed to set up the correct path above
import webvulnscan

__all__ = []


# A little function for help.
def gen_to_set(generator):
    return {x for x in generator}


def gen_to_dict(generator):
    return {x: y for x, y in generator}


# Random String generator for tokens, etc...
def random_string(length):
    return ''.join([random.choice('01234567890ABCDEF') for x in range(8)])


# custom loghandler which memorises every record.
class LogHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
        self.log_entrys = []

    def warning(self, record):
        self.log_entrys.extend([record])


# A class for writing site which are detemined
# to be request by webvulnscan.Client()
class ClientSite(object):
    def __init__(self):
        pass

    def download(self, url, parameters=None, remember_visited=None):
        pass

    def download_page(self, url, parameters=None, remember_visited=None):
        pass
