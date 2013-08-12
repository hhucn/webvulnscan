try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

from .form_input import FormInput


class Form(object):
    def __init__(self, url, document):
        self.document = document
        self.action = urljoin(url, document.attrib.get('action'))
        self.parameters = {}

    def get_inputs(self):
        for input_element in self.get_input_elements():
            yield FormInput(input_element)

    def get_parameters(self):
        for input_element in self.get_input_elements():
            form_input = FormInput(input_element)
            yield form_input.get_name(), form_input.get_type()

    def get_input_elements(self):
        for form_input in self.document.findall('.//input[@type]'):
            yield form_input

    def send(self, client, parameters):
        return client.download_page(self.action, parameters)
