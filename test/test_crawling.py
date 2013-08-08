import unittest
import xml.etree.ElementTree as ET

import tutil
from webvulnscan import crawling


class CrawlingTest(unittest.TestCase):
    def test_links_on_site(self):
        doc = ET.fromstring(
            '<html><a href="/x">link</a><a name="here">here</a></html>')
        self.assertEqual(list(crawling.links_on_site("http://test/", doc)),
                         ['http://test/x'])

    def test_inputs_on_form(self):
        def to_dict(generator):
            return {x: y for x, y in generator}
        # First, test for one element.
        one_element = ET.fromstring('<form action="random">'
                                    '<input name="button" type="submit">Hello!'
                                    '</input></form>')
        values = to_dict(crawling.inputs_in_form(one_element))
        self.assertEqual(values, {"button": "submit"})
        # Second, test with no inputs.
        zero_element = ET.fromstring('<form action="random"></form>')
        values = to_dict(crawling.inputs_in_form(zero_element))
        self.assertEqual(values, {})

    def test_forms_on_site(self):
        doc = ET.fromstring(
            '<html><form action="/x">'
            '<input type="text" name="test"></input>'
            '</form></html>')
        values = {x: y for x, y in crawling.forms_on_site("http://test", doc)}
        self.assertEqual(values, {"http://test/x": {"test": "text"}})

if __name__ == '__main__':
    unittest.main()
