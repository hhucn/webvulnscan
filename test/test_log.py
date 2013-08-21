import unittest

import sys
import tutil
from webvulnscan import print_logs
import webvulnscan.log


class LogTest(unittest.TestCase):
    def setUp(self):
        webvulnscan.log.do_print = True

    def test_warning(self):
        random_str = tutil.random_string(12)
        webvulnscan.log.warn("http://test", random_str)

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "Warning: http://test " + random_str)

    def test_vulnerability(self):
        random_str = tutil.random_string(12)
        webvulnscan.log.vulnerability("http://test", random_str)

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "Vulnerability: http://test " + random_str)

    def test_info(self):
        random_str = tutil.random_string(12)
        webvulnscan.log.info("http://test", random_str)

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "Information: http://test " + random_str)

    def test_log(self):
        random_str = tutil.random_string(12)
        webvulnscan.log.log(0, random_str, random_str)
        print_logs()

        output = sys.stdout.getvalue().strip()
        self.assertNotEqual(output, "")

        webvulnscan.log.log(0, random_str, random_str)
        print_logs()

        output = sys.stdout.getvalue().strip()
        self.assertNotEqual(output, "")




# To be written - Test log with actually big sizes of data.
#    def stress_test(self):
#        pass
