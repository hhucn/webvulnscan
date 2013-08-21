from ..log import warn
from ..utils import change_parameter, modify_parameter

SYMBOLS = {'\x00', u'\uFFFF'}


def try_on_form(client, form, symbol):
    parameters = dict(form.get_parameters())
    for parameter in parameters:
        attack_parameters = modify_parameter(parameters, parameter, symbol)
        result = form.send(client, attack_parameters)
        evaluate(form.action, result)


def try_on_url(client, url, parameter, symbol):
    attack_parameters = change_parameter(url, parameter, symbol)
    result = client.download_page(attack_parameters)
    evaluate(url, result)


def evaluate(target, result):
    if result.status_code == 500:
        warn(target, "Broken Unicode Handling", "Server return 500"
             " on invalid unicode character(s)")
    elif result.status_code == 200:
        warn(target, "Broken Unicode Handling", "Server accepts invalid"
             " unicode characters!")


def broken_unicode_characters(target_page, client):
    for symbol in SYMBOLS:
        for form in target_page.get_forms():
            try_on_form(client, form, symbol)

        for parameter in target_page.get_url_parameters:
            try_on_url(client, target_page.url, parameter, symbol)
