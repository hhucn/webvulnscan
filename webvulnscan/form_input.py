DEFAULT_TEXT_STRING = "abcdefgh"
DEFAULT_EMAIL_STRING = "ex@amp.le"


class FormInput(object):
    def __init__(self, element):
        self.element = element
        self.type_dictionary = {"text": DEFAULT_TEXT_STRING,
                                "email": DEFAULT_EMAIL_STRING}

    def get_type(self):
        current_type = self.element.attrib.get('type')
        if current_type is None:
            return ""
        else:
            return current_type.lower()

    def get_element_value(self):
        """ NOT FOR EXTERNAL USE """
        value = self.element.attrib.get('value')
        if value is None:
            return ""
        else:
            return value.lower()

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
