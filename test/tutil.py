""" Common test setup functions """

import logging
import os.path
import sys

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

# A util for testing functions with output.
class LogHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
