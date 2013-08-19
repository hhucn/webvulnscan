import unittest

import sys
import tutil
import webvulnscan.log


class LogTest(unittest.TestCase):
    def test_warning(self):
        random_str = tutil.random_string(12)
        webvulnscan.log.warn("http://test", random_str, random_str)

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "Warning: " + random_str
                         + "under http://test " + random_str)

    def test_vulnerability(self):
        random_str = tutil.random_string(12)
        webvulnscan.log.warn("http://test", random_str, random_str)

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "Vulnerability: " + random_str
                         + "under http://test " + random_str)

    def test_info(self):
        random_str = tutil.random_string(12)
        webvulnscan.log.warn("http://test", random_str, random_str)

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "Info: " + random_str
                         + "under http://test " + random_str)


# To be written - Test log with actually big sizes of data.
#    def stress_test(self):
#        pass
