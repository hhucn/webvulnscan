from ..utils import attack, change_parameter, modify_parameter

BODY = u'o'
CLRF_SEQUENCE = (
    u"Content-Type: text/html\r\n" +
    u"Content-Length: %d\r\n\r\n" % len(BODY))
ATTACK_SEQUENCE = CLRF_SEQUENCE + BODY


def attack_form(client, log, form):
    parameters = dict(form.get_parameters())
    for parameter in parameters:
        attack_parameters = modify_parameter(parameters, parameter,
                                             ATTACK_SEQUENCE)
        result = form.send(client, attack_parameters)
        evaluate(log, form.action, result)


def attack_url(client, log, url, parameter):
    attack_parameters = change_parameter(url, parameter, ATTACK_SEQUENCE)
    result = client.download_page(attack_parameters)
    evaluate(log, url, result)


def evaluate(log, target, result):
    if result.headers.get('Content-Length') == str(len(BODY)):
        log('vuln', target, u'CRLF Injection', request=result.request)
    elif result.status_code == 500:
        log('warn', target, u'Parameter Parsing Error', request=result.request)


def search(page):
    for form in page.get_forms():
        yield ('form', form)

    for parameter, _ in page.url_parameters:
        yield ('url', page.url, parameter)


@attack(search)
def crlf(client, log, target_type, *args):
    globals()['attack_' + target_type](client, log, *args)
