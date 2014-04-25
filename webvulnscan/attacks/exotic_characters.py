from ..utils import attack, change_parameter, modify_parameter, get_page_text

SYMBOLS = {
    u'"', u"'", u'<', u'{', u'(', u')', u'}', u'>', u'&', u'|', u';',
    u'\u1D550', u'\x00', u'\uFFFF'}
DETECT_STRING = "test"


def is_error_code(page):
    return page.status_code in [500, 503]


def attack_form(client, log, form, name, symbol):
    guessed_parameters = dict(form.get_parameters())
    parameters = modify_parameter(guessed_parameters, name,
                                  symbol)
    try:
        page = form.send(client, parameters)
    except Exception as e:
        log('vuln', form.action, 'Possible incorrect Unicode Handling',
            repr(symbol))
        return

    if is_error_code(page):
        log('vuln', form.action, 'Incorrect Unicode Handling', repr(symbol))


def attack_url(client, log, url, parameter):
    test_page = client.download_page(
        change_parameter(url, parameter, DETECT_STRING))
    if is_error_code(test_page):
        return

    for symbol in SYMBOLS:
        new_url = change_parameter(url, parameter, symbol.encode('utf-8'))
        attacked_page = client.download_page(new_url)

        if is_error_code(attacked_page):
            log('vuln', url, 'Incorrect Unicode handling in URL', repr(symbol))


def search(page):
    for form in page.get_forms():
        for name, _ in form.get_parameters():
            for symbol in SYMBOLS:
                yield ('form', form, name, symbol)

    for parameter, _ in page.url_parameters:
        yield('url', page.url, parameter)


@attack(search)
def exotic_characters(client, log, target_type, *args):
    globals()['attack_' + target_type](client, log, *args)
