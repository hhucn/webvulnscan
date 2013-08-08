import unittest
import xml.etree.ElementTree as ET

try:
    from urllib.parse import unquote
except ImportError:
    from urllib import unquote

import tutil
import webvulnscan


class XSSTest(unittest.TestCase):
    def test_xss(self):
        # We need a LogHandler to get view the output of the functions.
        class LogHandler(tutil.LogHandler):

            def __init__(self):
                self.found_xss = False
                tutil.LogHandler.__init__(self)

            def emit(self, record):
                self.found_xss = True

            def reset(self):
                self.found_xss = False

        # Here we hijack the logger.
        log = LogHandler()
        webvulnscan.attacks.XSS.__dict__['log'].addHandler(log)

        # Our first test case - no vulnerability.
        def no_vuln(url=None, parameters=None, cookies=None):
            return '<form action="/page">' + \
                   '<input name="random" type="text"></input>' + \
                   '</form>'

        # We need to monkey patch the get_plain_text function.
        webvulnscan.utils.__dict__['get_plain_text'] = no_vuln
        reload(webvulnscan.attacks.XSS)

        # Run the simulated attack.
        webvulnscan.attacks.XSS.xss(no_vuln(), [],
                                    {"/page": {"random": "text"}})
        self.assertEqual(log.found_xss, False)
        log.reset()

        # Second test case, a vulnerability in the url.
        def url_vuln(url="", parameters=None, cookies=None):
            if "=" in url:
                return unquote(url.split("=")[1])
            else:
                return "Here is nothing :("

        #  Monkey patch again...
        webvulnscan.utils.__dict__['get_plain_text'] = url_vuln
        reload(webvulnscan.attacks.XSS)
        webvulnscan.attacks.XSS.__dict__['log'].addHandler(log)

        # Run it!
        webvulnscan.attacks.XSS.xss("http://test/?test=random", ["test"], {})
        self.assertEqual(log.found_xss, True)
        log.reset()

        # Third test case, a post vulnerability.
        def post_vuln(url="", parameters={}, cookies=None):
            if parameters != {}:
                return list(parameters.items())[0][1]
            else:
                return "No post value?"

        # patching....
        webvulnscan.utils.__dict__['get_plain_text'] = post_vuln
        reload(webvulnscan.attacks.XSS)
        webvulnscan.attacks.XSS.__dict__['log'].addHandler(log)

        # Running...
        webvulnscan.attacks.XSS.xss("http://test/", [],
                                    {"test": {"random": "text"}})
        self.assertEqual(log.found_xss, True)
        log.reset()

        # Forth test case, both vulnerabilities.
        def combo_vuln(url="", parameters={}, cookies=None):
            return_str = ""
            if parameters != {}:
                return_str += list(parameters.items())[0][1]

            if "=" in url:
                return_str += unquote(url.split("=")[1])

            return return_str

        # patching....
        webvulnscan.utils.__dict__['get_plain_text'] = combo_vuln
        reload(webvulnscan.attacks.XSS)
        webvulnscan.attacks.XSS.__dict__['log'].addHandler(log)

        # Running...
        webvulnscan.attacks.XSS.xss("http://test/", [],
                                    {"test": {"random": "text"}})
        self.assertEqual(log.found_xss, True)
        log.reset()
