from ..log import vulnerability
from ..utils import change_parameter

SYMBOLS = {'"', "'", '<', '{', '(', ')', '}', '>', '&', '|', u"\U0001D550",
           u"\u0000"}
DETECT_STRING = "test"


def try_on_form(form, client, symbol):
        def modify_parameter(target_name, value):
            parameters = dict(form.get_parameters())
            parameters[target_name] = value
            return parameters

        parameters = modify_parameter(name, symbol)
        attacked_page = form.send(client, parameters)

        found = False
        for element in attacked_page.document.findall('.//*'):
            if element.text:
                if symbol in element:
                    found = True

        if not found:
            vulnerability(form.action, 'Incorrect Unicode Handling!')


def try_on_url(url, parameter, client, symbol):
    new_url = change_parameter(url, parameter, symbol)
    attacked_page = client.download_page(new_url)

    found = False
    for element in attacked_page.document.findall('.//*'):
        if element.text:
            if symbol in element.text:
                found = True

    if found:
        vulnerability(url, 'Incorrect Unicode handling in URL')


def exotic_charaters(target_page, client):
    print(target_page)
    for form in target_page.get_forms():
        def modify_parameter(target_name, value):
            parameters = dict(form.get_parameters())
            parameters[target_name] = value
            return parameters

        for name in form.get_parameters():
            test_value = modify_parameter(name, DETECT_STRING)
            value = form.send(client, test_value)

            test_found = False
            for element in value.document.findall('.//*'):
                if element.text:
                    if DETECT_STRING in element:
                        test_found = True

        if test_found:
            for symbol in SYMBOLS:
                try_on_form(form, client, symbol)

    for parameter, _ in target_page.get_url_parameters:
        test_value = change_parameter(target_page.url, parameter,
                                      DETECT_STRING)
        value = client.download_page(test_value)

        test_found = False
        for element in value.document.findall('.//*'):
            if element.text:
                if DETECT_STRING in element:
                    test_found = True

        if test_found:
            for symbol in SYMBOLS:
                try_on_url(target_page.url, parameter, client, symbol)

    print("over!")
