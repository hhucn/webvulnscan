import unittest
import xml.etree.ElementTree as ET

import tutil
from webvulnscan import utils


class UtilsTest(unittest.TestCase):

    def test_change_parameter(self):
        link = 'http://x.yz/?other=11&val=22'
        self.assertEqual(utils.change_parameter(link, "val", "42"),
                         'http://x.yz/?other=11&val=42')

    def test_get_url_host(self):
        link = 'http://random.host/test/value'
        self.assertEqual(utils.get_url_host(link), "random.host")
