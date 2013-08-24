from ..utils import attack, change_parameter, modify_parameter, get_page_text

SYMBOLS = {'"', "'", '<', '{', '(', ')', '}', '>', '&', '|', u'\u1D550'}
DETECT_STRING = "test"


def test_for_detect_form(form, name, client):
    test_value = modify_parameter(dict(form.get_parameters()), name,
                                  DETECT_STRING)
    value = form.send(client, test_value)

    for text in get_page_text(value):
        if DETECT_STRING in text:
            return True


def test_for_detect_url(url, parameter, client):
    test_value = change_parameter(url, parameter, DETECT_STRING)
    value = client.download_page(test_value)

    for element in get_page_text(value):
        if DETECT_STRING in element:
            return True


def attack_form(client, log, form, name, symbol):
    guessed_parameters = dict(form.get_parameters())
    parameters = modify_parameter(guessed_parameters, name,
                                  symbol)
    attacked_page = form.send(client, parameters)

    for text in get_page_text(attacked_page):
        if symbol in text:
            return

    log('vuln', form.action, 'Incorrect Unicode Handling', repr(symbol))


def attack_url(client, log, url, parameter):
    if not test_for_detect_url(url, parameter, client):
        return

    for symbol in SYMBOLS:
        new_url = change_parameter(url, parameter, symbol.encode('utf-8'))
        attacked_page = client.download_page(new_url)

        for element in get_page_text(attacked_page):
            if symbol in element:
                break
        else:
            log('vuln', url, 'Incorrect Unicode handling in URL', repr(symbol))


def search(page):
    for form in page.get_forms():
        for name, _ in form.get_parameters():
            for symbol in SYMBOLS:
                yield ('form', form, name, symbol)

    for parameter, _ in page.get_url_parameters:
        yield('url', page.url, parameter)


@attack(search)
def exotic_characters(client, log, target_type, *args):
    globals()['attack_' + target_type](client, log, *args)
