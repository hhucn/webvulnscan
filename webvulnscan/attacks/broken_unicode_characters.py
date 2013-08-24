from ..compat import quote_plus
from ..utils import attack, change_parameter, modify_parameter

SYMBOLS = {u'\x00', u'\uFFFF'}


def attack_form(client, log, form, symbol):
    parameters = dict(form.get_parameters())
    for parameter in parameters:
        symbol = quote_plus(symbol.encode('utf-8'))

        attack_parameters = modify_parameter(parameters, parameter, symbol)
        result = form.send(client, attack_parameters)
        evaluate(log, form.action, result)


def attack_url(client, log, url, parameter, symbol):
    attack_parameters = change_parameter(url, parameter, symbol)
    result = client.download_page(attack_parameters)
    evaluate(log, url, result)


def evaluate(log, target, result):
    if result.status_code == 500:
        log('warn', target, "Broken Unicode Handling",
            u'Server return 500 on invalid unicode character(s)')
    elif result.status_code == 200:
        log('warn', target, "Broken Unicode Handling",
            'Server accepts invalid unicode characters!')


def search(page):
    for form in page.get_forms():
        for symbol in SYMBOLS:
            yield ('form', form, symbol)

    for parameter in page.get_url_parameters:
        for symbol in SYMBOLS:
            yield ('url', page.url, parameter, symbol)


@attack(search)
def broken_unicode_characters(client, log, target_type, *args):
    globals()['attack_' + target_type](client, log, *args)
