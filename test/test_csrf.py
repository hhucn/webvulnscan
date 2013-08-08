import unittest
import xml.etree.ElementTree as ET

try:
    from urllib.parse import unquote 
except ImportError:
    from urllib import unquote

import random
import tutil
import webvulnscan

class TestCSRF(unittest.TestCase):
    def test_csrf(self):
        # We need a logging hijacker.
        class LogHandler(tutil.LogHandler):
            def __init__(self):
                self.found_csrf = False
                tutil.LogHandler.__init__(self)

            def emit(self, record):
                self.found_csrf = True

            def reset(self):
                self.found_csrf = False

        log = LogHandler()
        # Monkey patch the functions. 
        def hijack(function):
            webvulnscan.utils.__dict__['get_plain_text'] = function 
            reload(webvulnscan.attacks.CSRF)
            log.reset()
            webvulnscan.attacks.CSRF.__dict__['log'].addHandler(log)

        # First test Case, no forms.
        def no_form(url=None, parameters=None, cookies=None):
            return "Here is nothing."

        hijack(no_form)

        webvulnscan.attacks.csrf("test_case", {})
        self.assertEqual(log.found_csrf, False)

        # Second test Case, CSRF secured form.
        token = str([random.choice('abcdef0123456789') for x in range(8)])

        def secure_form(url=None, parameters={}, cookies=None):
            if "token" in parameters:
                if parameters["token"] == token:
                    return "Yay! This Connection is secure."
                else:
                    return None

        hijack(secure_form)

        webvulnscan.attacks.csrf("test_random", {"token": "text", "rand": "text"})
        self.assertEqual(log.found_csrf, False)

        # Third test Case, CSRF unsecure form.
        def unsecure_form(url=None, parameters={}, cookies=None):
            for parameter in parameters:
                return parameter

        hijack(unsecure_form)

        webvulnscan.attacks.csrf("test_random", {"token": "text", "rand": "text"})
        self.assertEqual(log.found_csrf, True)
