try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


class Form(object):
    def __init__(self, url, document):
        self.document = document
        self.action = urljoin(url, document.attrib.get('action'))
        self.parameters = {}

    def get_inputs(self):
        for form_input in self.document.findall('.//input[@type]'):
            form_input_type = form_input.attrib.get('type')
            form_input_name = form_input.attrib.get('name')
            yield form_input_name, form_input_type

    def send(self, client, parameters):
        return client.download_page(self.action, parameters)
