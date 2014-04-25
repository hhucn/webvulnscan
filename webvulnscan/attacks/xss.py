from ..utils import attack, change_parameter

XSS_STRING = u'<script>alert("XSS_STRING");</script>'


def attack_post(client, log, form):
    # A helper function for modifing values of the parameter list.
    def modify_parameter(target_name, value):
        parameters = dict(form.get_parameters())
        parameters[target_name] = value
        return parameters

    for parameter_name, parameter_value in form.get_parameters():
        # Replace value with XSS_STRING
        parameters = modify_parameter(parameter_name, XSS_STRING)

        # Send the form
        try:
            attacked_page = form.send(client, parameters)
        except Exception as e:
            log('warn', form.action,
                'HTTP Errors occurs when confronted with html input',
                "in parameter" + parameter_name)
            return

        # Determine if the string is unfiltered on the page.
        if XSS_STRING in attacked_page.html:
            # Oh no! It is!
            log('vuln', attacked_page.url, "XSS",
                "in parameter " + parameter_name)


def attack_get(client, log, url, parameter):
    # Replace the value of the parameter with XSS_STRING
    attack_url = change_parameter(url, parameter, XSS_STRING)
    # To run the attack, we just request the site.
    attacked_page = client.download_page(attack_url)
    # If XSS_STRING is found unfilitered in the site, we have a problem.
    if XSS_STRING in attacked_page.html:
        log('vuln', attacked_page.url, "XSS", "in URL parameter " + parameter)


def search(page):
    for form in page.get_forms():
        yield ('post', form)

    for parameter, _ in page.url_parameters:
        yield ('get', page.url, parameter)


@attack(search)
def xss(client, log, target_type, *args):
    globals()['attack_' + target_type](client, log, *args)
