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

    @property
    def minlength(self):
        try:
            return int(self._get_attrib_value('minlength'))
        except ValueError:
            return 0

    @property
    def maxlength(self):
        try:
            return int(self._get_attrib_value('maxlength'))
        except ValueError:
            return 0

    def guess_value(self):
        value = self.type_dictionary.get(self.get_type, '')
        supposed_value = self._get_attrib_value("value")

        if supposed_value:
            next_value = supposed_value
        else:
            next_value = value

        if self.get_type == "text":
            if self.maxlength < len(next_value) and not self.maxlength == 0:
                next_value = value[:self.maxlength]

            if self.minlength > len(next_value) and not self.minlength == 0:
                if len(next_value) != 0:
                    required = len(next_value) - self.minlength \
                        / len(next_value)
                    next_value = value.join(value[0] * int(required))

        return next_value
