import unittest

import sys
import tutil
import webvulnscan.log


class LogTest(unittest.TestCase):
    def test_warning(self):
        random_str = tutil.random_string(12)
        webvulnscan.log.warn(random_str)
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "Warning: " + random_str)

    def test_vulnerability(self):
        random_str = tutil.random_string(12)
        webvulnscan.log.vulnerability(random_str)
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "Vulnerability: " + random_str)

    def test_info(self):
        random_str = tutil.random_string(12)
        webvulnscan.log.info(random_str)
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "Information: " + random_str)
