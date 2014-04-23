#!/usr/bin/env python3
from __future__ import unicode_literals

import unittest
import BaseHTTPServer
import urlparse
import tutil
import cgi
import os
import socket

import webvulnscan

sitemap = {}


class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
    def _default_page(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write("""
        <!DOCTYPE html>
        <html>
            <head>
                <title>webvulnscan tests</title>
            </head>
            <body>
                <h1>webvulnscan tests</h1>

                <ul> """)

        for x in sorted(sitemap):
            name = x
            self.wfile.write('<li><a href="' + cgi.escape(name) +
                             '/">' + cgi.escape(name) + '</a></li>')

        self.wfile.write("""
                </ul>
</body>
</html>
                        """)

    def _serve_request(self):
        parsed_path = urlparse.urlparse(self.path)

        if parsed_path.path == "/":
            self._default_page()
        else:
            current_path = parsed_path.path.split('/')[1]

            extended_path = "".join(parsed_path.path.split('/')[2:])

            site = sitemap[current_path]
            client = tutil.TestClient(site.urlmap)

            if parsed_path.query == "":
                url = "http://test.webvulnscan/" + extended_path
            else:
                url = "http://test.webvulnscan/" + extened_path +
                "?" + parsed_path.query

            request = webvulnscan.request.Request(url)

            if self.headers.getheader('content-length'):
                content_len = int(self.headers.getheader('content-length'))
                body = self.rfile.read(content_len)
                request.parameters = urlparse.parse_qs(body)

                for value in request.parameters:
                    modified_value = "".join(request.parameters[value])
                    request.parameters[value] = modified_value

            _, status_code, response_data, headers = client._download(request)
            self.send_response(status_code)
            for header in headers:
                self.send_header(header[0], header[1])
            self.end_headers()

            self.wfile.write(response_data)

    def handle_one_request(self):
        try:
            self.raw_requestline = self.rfile.readline(65537)
            if len(self.raw_requestline) > 65536:
                self.requestline = ''
                self.request_version = ''
                self.command = ''
                self.send_error(414)
                return
            if not self.raw_requestline:
                self.close_connection = 1
                return
            if not self.parse_request():
                return

            self._serve_request()
            self.wfile.flush()
        except socket.timeout as e:
            self.log_error("Request timed out: %r", e)
            self.close_connection = 1
            return


def discover():
    testloader = unittest.TestLoader()
    tests = testloader.discover(os.path.dirname(os.path.abspath(__file__)))
    for suite in tests:
        for klass in suite:
                for test in klass._tests:
                    elements = dir(test)
                    for subklass in elements:
                        func = getattr(test, subklass)
                        if hasattr(func, "urlmap"):
                            yield func


def main():
    for test in discover():
        sitemap[test.name] = test

    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class(("", 8000), Handler)
    httpd.serve_forever()

if __name__ == "__main__":
    main()
