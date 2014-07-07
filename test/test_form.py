import unittest
import xml.etree.ElementTree as ET

import tutil
import webvulnscan.form


class FormTest(unittest.TestCase):
    def test_no_inputs_no_action(self):
        doc = ET.fromstring('<form></form>')
        form = webvulnscan.form.Form('http://test/', doc)
        self.assertEqual({}, dict(form.get_inputs()))
        self.assertEqual("http://test/", form.action)

    def test_no_inputs_with_Action(self):
        doc = ET.fromstring('<form action="test"></form>')
        form = webvulnscan.form.Form('http://test/', doc)
        self.assertEqual(doc.items(), form.document.items())
        self.assertEqual(doc.keys(), form.document.keys())
        self.assertEqual("http://test/test", form.action)
        self.assertEqual("get", form.method)

    def test_one_input_no_action(self):
        doc = '<form><input type="text" name="test"></input></form>'
        doc = ET.fromstring(doc)
        form = webvulnscan.form.Form('http://test/', doc)
        self.assertEqual({"test": "abcdefgh"},
                         dict(form.get_parameters()))
        self.assertEqual("http://test/", form.action)

    def test_one_input_with_action(self):
        doc = '<form action="test"><input type="text" name="test">' \
              '</input></form>'
        doc = ET.fromstring(doc)
        form = webvulnscan.form.Form('http://test/', doc)
        self.assertEqual({"test": "abcdefgh"},
                         dict(form.get_parameters()))
        self.assertEqual("http://test/test", form.action)

    def test_serveral_inputs_no_action(self):
        doc = '<form><input type="text" name="test"></input>' \
              '<input type="submit" name="click"></input></form>'
        doc = ET.fromstring(doc)
        form = webvulnscan.form.Form('http://test/', doc)
        self.assertEqual({"test": "abcdefgh", "click": ""},
                         dict(form.get_parameters()))
        self.assertEqual("http://test/", form.action)

    def test_serveral_inputs_with_action(self):
        doc = '<form action="action"><input type="text" name="test"> ' \
              '</input><input type="submit" name="click"></input></form>'
        doc = ET.fromstring(doc)
        form = webvulnscan.form.Form('http://test/', doc)
        self.assertEqual({"test": "abcdefgh", "click": ""},
                         dict(form.get_parameters()))
        self.assertEqual("http://test/action", form.action)

    def test_form_with_textarea(self):
        doc = '<form action="action">' + \
              '<textarea name="test" placeholder="random" /></form>'
        doc = ET.fromstring(doc)
        form = webvulnscan.form.Form('http://test/', doc)
        self.assertEqual({"test": "random"},
                         dict(form.get_parameters()))
        self.assertEqual("http://test/action", form.action)

    def test_form_get_send(self):
        assert_function = self.assertEqual

        class StaticSite(object):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                assert_function("random" in url, True)

        doc = '<form method="get"><input type="text" name="test" ' + \
              'value="random"></input></form>'
        doc = ET.fromstring(doc)
        form = webvulnscan.form.Form('http://test/', doc)
        parameters = dict(form.get_parameters())
        form.send(StaticSite(), parameters)

    def test_form_post_send(self):
        assert_function = self.assertNotEqual

        class StaticSite(object):
            def download_page(self, url, parameters=None,
                              remember_visited=None):
                assert_function(parameters, None)

        doc = '<form method="post"><input type="text" name="test" ' + \
              'value="random"></input></form>'
        doc = ET.fromstring(doc)
        form = webvulnscan.form.Form('http://test/', doc)
        parameters = dict(form.get_parameters())
        form.send(StaticSite(), parameters)

    def test_search_form_class(self):
        doc = '<form class="search"></form>'
        doc = ET.fromstring(doc)
        form = webvulnscan.form.Form('http://test/', doc)
        self.assertEqual(form.is_search_form, True)

    def test_search_form_role(self):
        doc = '<form role="search"></form>'
        doc = ET.fromstring(doc)
        form = webvulnscan.form.Form('http://test/', doc)
        self.assertEqual(form.is_search_form, True)
