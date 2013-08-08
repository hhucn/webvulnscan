import unittest
import xml.etree.ElementTree as ET

import tutil
from webvulnscan import utils


class UtilsTest(unittest.TestCase):
    def test_find_parameter_values(self):
        two_parameter = 'http://random.host/?x=y&z=x'
        values_two = [x for x in utils.find_parameter_values(two_parameter)]
        self.assertEqual(values_two, ["y", "x"])
        no_parameter = 'http://random.host/test/'
        values_no = [x for x in utils.find_parameter_values(no_parameter)]
        self.assertEqual(values_no, [])

    def test_change_parameter(self):
        link = 'http://x.yz/?val=22&other=11'
        self.assertEqual(utils.change_parameter(link, "val", "42"),
                         'http://x.yz/?val=42&other=11')

    def test_get_url_host(self):
        link = 'http://random.host/test/value'
        self.assertEqual(utils.get_url_host(link), "random.host")
