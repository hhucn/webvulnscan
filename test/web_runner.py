#!/usr/bin/env python3
from __future__ import unicode_literals

import unittest
import tutil
import cgi
import os
import socket

try:
    from http.server import BaseHTTPRequestHandler, HTTPServer
except ImportError:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

try:
    from urllib.parse import urlparse, parse_qs
except ImportError:
    from urlparse import urlparse, parse_qs

import webvulnscan

sitemap = {}


class Handler(BaseHTTPRequestHandler):
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

                <ul> """.encode("utf-8"))

        for x in sorted(sitemap):
            name = x
            self.wfile.write('<li><a href="'.encode("utf-8") +
                             cgi.escape(name).encode("utf-8") +
                             '/">'.encode("utf-8") +
                             cgi.escape(name).encode("utf-8") +
                             '</a></li>'.encode("utf-8"))

        self.wfile.write("""
                </ul>
</body>
</html>
                        """.encode("utf-8"))

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
            for header in headers:
                self.send_header(header[0], header[1])
            self.end_headers()

            self.wfile.write(response_data)
        else:
            self.send_error(404, "File not Found!")

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
    suites = testloader.discover(os.path.dirname(os.path.abspath(__file__)))
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

    server_class = HTTPServer
    httpd = server_class(("", 8000), Handler)
    httpd.serve_forever()

if __name__ == "__main__":
    main()
