""" Common test setup functions """

import logging
import os.path
import sys

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

# If this fails, we failed to set up the correct path above
import webvulnscan

__all__ = []


# A util for testing functions with output.
class LogHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
