import unittest
import xml.etree.ElementTree

import tutil
import utils


class UtilsTest(unittest.TestCase):
    def test_find_get_parameters(self):
        link = 'http://random.host/?x=y&z=x'
        self.assertEqual(utils.find_get_parameters(link), ["x", "z"])

    def test_change_parameter(self):
        link = 'http://x.yz/?val=22&other=11'
        self.assertEqual(utils.change_parameter(link, "val", "42"),
                         'http://x.yz/?val=42&other=11')

    def test_get_url_host(self):
        link = 'http://random.host/test/value'
        self.assertEqual(utils.get_url_host(link), "random.host")
