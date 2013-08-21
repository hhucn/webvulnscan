from .compat import HTMLParser

import collections
import xml.etree.ElementTree
from . import log


class EtreeParser(HTMLParser):
    def __init__(self, url, log=log):
        # We need this ancient super form because HTMLParser is a
        # classic class in 2.x
        HTMLParser.__init__(self)
        self.tb = xml.etree.ElementTree.TreeBuilder()
        self.tag_stack = collections.deque()
        self.url = url
        self._log = log

    def handle_starttag(self, tag, attrs):
        self.tag_stack.append(tag)
        self.tb.start(tag, dict(attrs))

    def handle_endtag(self, tag):
        try:
            expected = self.tag_stack.pop()
        except IndexError:
            self._log.warn(
                self.url, "HTML Error",
                u"Tried to close tag <%s> after root element" % (tag,))
            return

        if expected != tag:
            if tag in self.tag_stack:
                # Someone forgot to close a tag
                while expected != tag:
                    self._log.warn(
                        self.url, "HTML Error",
                        u"Unclosed tag <%s>" % expected)
                    self.tb.end(expected)
                    expected = self.tag_stack.pop()
            else:
                # Random closing tag
                self._log.warn(
                    self.url, "HTML Error",
                    u"Encountered </%s>, expected </%s>" % (tag, expected))
                # Re-add the expected element in order to suppress
                # further errors
                self.tag_stack.append(expected)
                return

        self.tb.end(tag)

    def handle_data(self, data):
        self.tb.data(data)

    def close(self):
        HTMLParser.close(self)
        try:
            return self.tb.close()
        except AssertionError as error:
            self._log.warn(self.url, "HTML Error", error.message)
            raise
