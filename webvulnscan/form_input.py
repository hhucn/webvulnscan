DEFAULT_TEXT_STRING = "abcdefgh"
DEFAULT_EMAIL_STRING = "ex@amp.le"


class FormInput(object):
    def __init__(self, element):
        self.element = element
        self.type_dictionary = {"text": DEFAULT_TEXT_STRING,
                                "email": DEFAULT_EMAIL_STRING}

    def _get_attrib_value(self, name):
        value = self.element.attrib.get(name)

        if value is None:
            return ""
        else:
            return value

    def get_type(self):
        return self._get_attrib_value('type').lower()

    def get_name(self):
        return self._get_attrib_value('name')

    def get_element_value(self):
        return self._get_attrib_value('value')

    def guess_value(self):
        current_value = self.get_element_value()
        if current_value == "":
            for key, entry in self.type_dictionary.items():
                if key == self.get_type():
                    return entry

            # If no hit occured, we return simply ""
            return ""
        else:
            return current_value
