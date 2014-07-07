from .compat import urlencode, urljoin
from .utils import add_get_params

from .form_input import FormInput
from .textarea import TextArea


class Form(object):
    def __init__(self, url, document):
        self.document = document
        self.action = urljoin(url, document.attrib.get('action'))
        self.parameters = {}

    @property
    def method(self):
        return self.document.attrib.get('method', 'get').lower()

    @property
    def is_search_form(self):
        role = self.document.attrib.get('role', '').lower()
        form_class = self.document.attrib.get('class', '').lower()
        return role == "search" or form_class == "search"

    def get_inputs(self):
        for input_element in self.get_input_elements():
            yield FormInput(input_element)

        for textarea in self.get_textarea_elements():
            yield TextArea(textarea)

    def get_parameters(self):
        for item in self.get_inputs():
            yield (item.get_name, item.guess_value())

    def get_input_elements(self):
        for form_input in self.document.findall('.//input'):
            yield form_input

    def get_textarea_elements(self):
        for textarea in self.document.findall('.//textarea'):
            yield textarea

    def send(self, client, parameters):
        if self.method == "get":
            url = add_get_params(self.action, parameters)
            return client.download_page(url)
        else:
            return client.download_page(self.action, parameters)
