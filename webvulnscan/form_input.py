from .log import warn


class FormInput(object):
    def __init__(self, element):
        self.element = element
        self.type_dictionary = {"text": "abcdefgh",
                                "email": "ex@amp.le",
                                "password": "abcd1234",
                                "checkbox": "true",
                                "radio": "1",
                                "datetime": "1990-12-31T23:59:60Z",
                                "datetime-local":
                                "1985-04-12T23:20:50.52",
                                "date": "1996-12-19",
                                "month": "1996-12",
                                "time": "13:37:00",
                                "week": "1996-W16",
                                "number": "123456",
                                "range": "1.23",
                                "url": "http://localhost/",
                                "search": "query",
                                "tel": "012345678",
                                "color": "#FFFFFF",
                                "hidden": "Secret.",
                                "submit": ""}

    def _get_attrib_value(self, name):
        return self.element.attrib.get(name, "")

    @property
    def get_type(self):
        return self._get_attrib_value('type').lower()

    @property
    def get_name(self):
        return self._get_attrib_value('name')

    @property
    def get_element_value(self):
        return self._get_attrib_value('value')

    def guess_value(self):
        value = self.type_dictionary.get(self.get_type, '')
        supposed_value = self._get_attrib_value("value")
        if supposed_value:
            return supposed_value
        elif value:
            return value
        else:
            warn("Warning: Unkown value!")
            return ""
