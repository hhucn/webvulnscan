from .compat import HTMLParser

import xml.etree.ElementTree
from .log import warn


class EtreeParser(HTMLParser):
    def __init__(self, url):
        # We need this anicient super form because HTMLParser is a
        # classic class in 2.x
        HTMLParser.__init__(self)
        self.tb = xml.etree.ElementTree.TreeBuilder()
        self.tag_dictionary = {}
        self.url = url

    def handle_starttag(self, tag, attrs):
        if tag in self.tag_dictionary:
            self.tag_dictionary[tag] += 1
        else:
            self.tag_dictionary[tag] = 0

        self.tb.start(tag, dict(attrs))

    def handle_endtag(self, tag):
        if tag in self.tag_dictionary:
            self.tag_dictionary[tag] -= 1
        else:
            warn(self.url, "HTML Error", "Tried to close Tag <" + tag +
                 ">, which where never opened")
            exit(2)

        if self.tag_dictionary[tag] < -1:
            warn(self.url, "HTML Error",  "Tag <" + tag + "> was more closed"
                 " then opened")
            exit(2)

        try:
            self.tb.end(tag)
        except AssertionError as error:
            warn(self.url, "HTML Error", error.message)
            exit(2)

    def handle_data(self, data):
        self.tb.data(data)

    def close(self):
        HTMLParser.close(self)
        try:
            return self.tb.close()
        except AssertionError as error:
            warn(self.url, "HTML Error", error.message)
            exit(2)
