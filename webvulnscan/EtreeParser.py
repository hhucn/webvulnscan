try:
    from html.parser import HTMLParser
except ImportError:  # Python < 3
    from HTMLParser import HTMLParser
import xml.etree.ElementTree


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
            print("HTML error: Tried to close Tag <" + tag + ">, which where"
                  "never opened in " + self.url)
            exit(2)

        if self.tag_dictionary[tag] < -1:
            print("HTML error: Tag <" + tag + "> was more closed than "
                  "than opened in " + self.url)
            exit(2)

        self.tb.end(tag)

    def handle_data(self, data):
        self.tb.data(data)

    def close(self):
        HTMLParser.close(self)
        return self.tb.close()
