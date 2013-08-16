import unittest

import tutil
from webvulnscan import utils


class UtilsTest(unittest.TestCase):

    def test_change_parameter(self):
        link = 'http://x.yz/?other=11&val=22'
        generated = utils.change_parameter(link, "val", "42")
        if "22" in generated:
            self.assertEqual(-1, 1)

    def test_get_url_host(self):
        link = 'http://random.host/test/value'
        self.assertEqual(utils.get_url_host(link), "random.host")
