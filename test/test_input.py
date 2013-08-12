import unittest
import xml.etree.ElementTree as ET

import tutil
import webvulnscan.form_input


class InputTest(unittest.TestCase):
    def test_input_disabled(self):
        doc = ET.fromstring('<input disabled="disabled"></input>')
        form_input = webvulnscan.form_input.FormInput(doc)
        self.assertEqual(form_input.guess_value(), "")

    def test_input_no_meanings(self):
        doc = ET.fromstring('<input></input>')
        form_input = webvulnscan.form_input.FormInput(doc)
        self.assertEqual(form_input.guess_value(), "")

    def test_input_text_no_value(self):
        doc = ET.fromstring('<input type="text"></input>')
        form_input = webvulnscan.form_input.FormInput(doc)
        self.assertEqual(form_input.guess_value(), "abcdefgh")

    def test_input_text_with_value(self):
        doc = ET.fromstring('<input type="text" value="hgfedcba"></input>')
        form_input = webvulnscan.form_input.FormInput(doc)
        self.assertEqual(form_input.guess_value(), "hgfedcba")

    def test_input_email_no_value(self):
        doc = ET.fromstring('<input type="email"></input>')
        form_input = webvulnscan.form_input.FormInput(doc)
        self.assertEqual(form_input.guess_value(), "ex@amp.le")

    def test_input_email_with_value(self):
        doc = ET.fromstring('<input type="email" value="ad@ministrat.or">'
                            '</input>')
        form_input = webvulnscan.form_input.FormInput(doc)
        self.assertEqual(form_input.guess_value(), "ad@ministrat.or")
