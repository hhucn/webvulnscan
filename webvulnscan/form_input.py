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
                                "color": "#FFFFFF"}

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
        current_value = self.get_element_value
        if current_value == "":
            for key, entry in self.type_dictionary.items():
                if key == self.get_type:
                    return entry

            # If no hit occured, we return simply ""
            return ""
        else:
            return current_value
