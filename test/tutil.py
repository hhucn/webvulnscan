""" Common test setup functions """

import os.path
import sys

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(root_dir, 'src'))

# If this fails, we failed to set up the correct path above
import webvulnscan

__all__ = []
