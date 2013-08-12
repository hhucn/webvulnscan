import unittest
import xml.etree.ElementTree as ET

import tutil
import webvulnscan.form


class FormTest(unittest.TestCase):
    def test_no_inputs_no_action(self):
        doc = ET.fromstring('<form></form>')
        form = webvulnscan.form.Form('http://test/', doc)
        self.assertEqual({}, tutil.gen_to_dict(form.get_inputs()))
        self.assertEqual("http://test/", form.action)

    def test_no_inputs_with_Action(self):
        doc = ET.fromstring('<form action="test"></form>')
        form = webvulnscan.form.Form('http://test/', doc)
        self.assertEqual(doc.items(), form.document.items())
        self.assertEqual(doc.keys(), form.document.keys())
        self.assertEqual("http://test/test", form.action)

    def test_one_input_no_action(self):
        doc = '<form><input type="text" name="test"></input></form>'
        doc = ET.fromstring(doc)
        form = webvulnscan.form.Form('http://test/', doc)
        self.assertEqual({"test": "text"},
                         tutil.gen_to_dict(form.get_parameters()))
        self.assertEqual("http://test/", form.action)

    def test_one_input_with_action(self):
        doc = '<form action="test"><input type="text" name="test">' \
              '</input></form>'
        doc = ET.fromstring(doc)
        form = webvulnscan.form.Form('http://test/', doc)
        self.assertEqual({"test": "text"},
                         tutil.gen_to_dict(form.get_parameters()))
        self.assertEqual("http://test/test", form.action)

    def test_serveral_inputs_no_action(self):
        doc = '<form><input type="text" name="test"></input>' \
              '<input type="submit" name="click"></input></form>'
        doc = ET.fromstring(doc)
        form = webvulnscan.form.Form('http://test/', doc)
        self.assertEqual({"test": "text", "click": "submit"},
                         tutil.gen_to_dict(form.get_parameters()))
        self.assertEqual("http://test/", form.action)

    def test_serveral_inputs_with_action(self):
        doc = '<form action="action"><input type="text" name="test"> ' \
              '</input><input type="submit" name="click"></input></form>'
        doc = ET.fromstring(doc)
        form = webvulnscan.form.Form('http://test/', doc)
        self.assertEqual({"test": "text", "click": "submit"},
                         tutil.gen_to_dict(form.get_parameters()))
        self.assertEqual("http://test/action", form.action)
