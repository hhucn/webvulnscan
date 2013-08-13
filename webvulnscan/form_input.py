DEFAULT_TEXT_STRING = "abcdefgh"
DEFAULT_EMAIL_STRING = "ex@amp.le"
DEFAULT_PASSWORD_STRING = "abcd1234"
DEFAULT_CHECKBOX_STRING = "true"
DEFAULT_RADIO_STRING = "1"
DEFAULT_DATETIME_STRING = "1990-12-31T23:59:60Z"
DEFAULT_DATETIME_LOCAL_STRING = "1985-04-12T23:20:50.52"
DEFAULT_DATE_STRING = "1996-12-19"
DEFAULT_MONTH_STRING = "1996-12"
DEFAULT_TIME_STRING = "13:37:00"
DEFAULT_WEEK_STRING = "1996-W16"
DEFAULT_NUMBER_STRING = "123456"
DEFAULT_RANGE_STRING = "1.23"
DEFAULT_URL_STRING = "http://localhost/"
DEFAULT_SEARCH_STRING = "query"
DEFAULT_TEL_STRING = "012345678"
DEFAULT_COLOR_STRING = "#FFFFFF"


class FormInput(object):
    def __init__(self, element):
        self.element = element
        self.type_dictionary = {"text": DEFAULT_TEXT_STRING,
                                "email": DEFAULT_EMAIL_STRING,
                                "password": DEFAULT_PASSWORD_STRING,
                                "checkbox": DEFAULT_CHECKBOX_STRING,
                                "radio": DEFAULT_RADIO_STRING,
                                "datetime": DEFAULT_DATETIME_STRING,
                                "datetime-local":
                                DEFAULT_DATETIME_LOCAL_STRING,
                                "date": DEFAULT_DATE_STRING,
                                "month": DEFAULT_MONTH_STRING,
                                "time": DEFAULT_TIME_STRING,
                                "week": DEFAULT_WEEK_STRING,
                                "number": DEFAULT_NUMBER_STRING,
                                "range": DEFAULT_RANGE_STRING,
                                "url": DEFAULT_URL_STRING,
                                "search": DEFAULT_SEARCH_STRING,
                                "tel": DEFAULT_TEL_STRING,
                                "color": DEFAULT_COLOR_STRING}

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
