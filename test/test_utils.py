import unittest
import xml.etree.ElementTree as ET

import tutil
from webvulnscan import utils


class UtilsTest(unittest.TestCase):
    def test_find_get_parameters(self):
        link = 'http://random.host/?x=y&z=x'
        self.assertEqual(utils.find_get_parameters(link), ["x", "z"])

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

    def test_get_page(self):
        # First, test for valid XML input.
        def get_plain_text(url, parameters=None, cookies=None):
            return "<html><a></a></html>"
        utils.get_plain_text = get_plain_text
        expect = ET.tostring(ET.fromstring(get_plain_text("")))
        result = ET.tostring(utils.get_page("http://x/"))
        self.assertEqual(expect, result)
        # Second, test for wrong input.
        def get_plain_none(url, parameters=None, cookies=None):
            return None
        utils.get_plain_text = get_plain_none
        self.assertEqual(None, utils.get_page("http://test/"))
