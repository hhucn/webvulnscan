#!/usr/bin/env python3
from __future__ import unicode_literals

import cgi
import io
import os
import socket
import unittest
import sys

try:
    from http.server import BaseHTTPRequestHandler, HTTPServer
except ImportError:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

try:
    from urllib.parse import urlparse, parse_qs
except ImportError:
    from urlparse import urlparse, parse_qs

_WVS_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(_WVS_ROOT_DIR)
import webvulnscan

sitemap = {}


class WebRunnerHandler(BaseHTTPRequestHandler):
    def _write(self, s):
        return self.wfile.write(s.encode('utf-8'))

    def _default_page(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        w = self._write
        w("""<!DOCTYPE html>
        <html>
            <head>
                <meta charset="utf-8" />
                <title>webvulnscan tests</title>
            </head>
            <body>
                <h1>webvulnscan tests</h1>

                <ul>
        """)

        for name in sorted(sitemap):
            w('<li><a href="' + cgi.escape(name, quote=True) + '/">')
            w(cgi.escape(name))
            w('</a></li>')

        w("""
                </ul>
            </body>
            </html>""")

    def _serve_request(self):
        parsed_path = urlparse(self.path)
        current_path = parsed_path.path.split('/')[1]

        if parsed_path.path == "/":
            self._default_page()
        elif current_path in sitemap:
            extended_path = "".join(parsed_path.path.split('/')[2:])

            site = sitemap[current_path]
            client = site.client

            if parsed_path.query == "":
                url = "http://test.webvulnscan/" + extended_path
            else:
                url = "http://test.webvulnscan/" + extended_path +\
                    "?" + parsed_path.query

            request = webvulnscan.request.Request(url)

            if 'content-length' in self.headers:
                content_len = int(self.headers['content-length'])
                body = self.rfile.read(content_len)
                request.parameters = parse_qs(body)

                for value in request.parameters:
                    new_value = request.parameters[value][0].decode('utf-8')
                    request.parameters[value] = new_value

            _, status_code, response_data, headers = client._download(request)
            self.send_response(status_code)
            self.send_header('Content-Type', 'text/html')
            for header in headers:
                self.send_header(header[0], header[1])
            self.end_headers()

            self.wfile.write(response_data)
        else:
            self.send_error(404, "File not Found!")

    def __getattr__(self, name):
        if name.startswith('do_'):
            return self._serve_request
        raise AttributeError()


def discover():
    testloader = unittest.TestLoader()
    suites = testloader.discover(os.path.join(_WVS_ROOT_DIR, 'test'))
    for suite in suites:
        for klass in suite:
            for test in klass._tests:
                elements = dir(test)
                for subklass in elements:
                    func = getattr(test, subklass)
                    if hasattr(func, "client"):
                        yield func


def main():
    for test in discover():
        sitemap[test.__name__] = test

    httpd = HTTPServer(("", 8000), WebRunnerHandler)
    httpd.serve_forever()

if __name__ == "__main__":
    main()
