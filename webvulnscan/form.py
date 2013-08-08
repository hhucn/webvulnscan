try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


def Form(object):
    def __init__(self, url, document):
        self.document = document
        self.action = document.attrib.get('action')
        self.parameters = {}

    def inputs(self):
        for link in self.document.findall('.//a[@href]'):
            href = link.attrib.get('href')
            yield urljoin(self.url, href)

    def send(self, client, parameters):
        return client.download_page(self.action, parameters)
