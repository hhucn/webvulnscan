import unittest

import tutil
import xml.etree.ElementTree as ET
from webvulnscan import utils


class SimulatedPage(object):
    def __init__(self, document):
        self.document = document


class UtilsTest(unittest.TestCase):
    def test_change_parameter_with_query(self):
        link = 'http://x.yz/?other=11&val=22&yet=3'
        generated = utils.change_parameter(link, "val", "42")
        self.assertTrue('val=22' not in generated)
        self.assertTrue('val=42' in generated)
        self.assertTrue('other=11' in generated)
        self.assertTrue('yet=3' in generated)

    def test_change_parameter_no_query(self):
        link = 'http://x.yz/'
        generated = utils.change_parameter(link, "val", "42")
        self.assertEqual(generated, link)

    def test_get_url_host(self):
        link = 'http://random.host/test/value'
        self.assertEqual(utils.get_url_host(link), "random.host")

    def test_get_page_text_no_text(self):
        doc = ET.fromstring('<head><sub></sub></head>')
        page = SimulatedPage(doc)
        self.assertEqual(list(utils.get_page_text(page)), [])

    def test_get_page_text_with_text(self):
        doc = ET.fromstring('<head>text<sub>subtext</sub></head>')
        page = SimulatedPage(doc)
        self.assertEqual(list(utils.get_page_text(page)),
                         ['text', 'subtext'])

    def test_modify_parameters(self):
        parameters = {'test': 'abc', 'test2': 'cba'}
        new_parameters = utils.modify_parameter(parameters,
                                                'test', 'cba')
        parameter_list = list(new_parameters.values())
        self.assertEqual(parameter_list, ['cba', 'cba'])
