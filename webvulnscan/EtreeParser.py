try:
    from html.parser import HTMLParser
except ImportError:  # Python < 3
    from HTMLParser import HTMLParser
import xml.etree.ElementTree


class EtreeParser(HTMLParser):
    def __init__(self):
        # We need this anicient super form because HTMLParser is a
        # classic class in 2.x
        HTMLParser.__init__(self)
        self.tb = xml.etree.ElementTree.TreeBuilder()

    def handle_starttag(self, tag, attrs):
        self.tb.start(tag, dict(attrs))

    def handle_endtag(self, tag):
        self.tb.end(tag)

    def handle_data(self, data):
        self.tb.data(data)

    def close(self):
        HTMLParser.close(self)
        return self.tb.close()
