from ..utils import change_parameter
from ..log import vulnerability

XSS_STRING = '<script>alert("XSS_STRING");</script>'


def try_post_xss(form, client):
    # A helper function for modifing values of the parameter list.
    def modify_parameter(target_name, value):
        parameters = dict(form.get_parameters())
        parameters[target_name] = value
        return parameters

    for parameter_name, parameter_value in form.get_parameters():
        # Replace value with XSS_STRING
        parameters = modify_parameter(parameter_name, XSS_STRING)

        # Send the form
        attacked_page = form.send(client, parameters)

        # Determine if the string is unfiltered on the page.
        if XSS_STRING in attacked_page.html:
            # Oh no! It is!
            vulnerability(attacked_page.url, "XSS",
                          "in parameter " + parameter_name)


def try_get_xss(url, parameter, client):
    # Replace the value of the parameter with XSS_STRING
    attack_url = change_parameter(url, parameter, XSS_STRING)
    # To run the attack, we just request the site.
    attacked_page = client.download_page(attack_url)
    # If XSS_STRING is found unfilitered in the site, we have a problem.
    if XSS_STRING in attacked_page.html:
        # Theres something wrong.
        vulnerability(attacked_page.url, "XSS",
                      "in URL parameter " + parameter)


def xss(target_page, client):
    for form in target_page.get_forms():
        try_post_xss(form, client)

    for parameter, _ in target_page.get_url_parameters:
        try_get_xss(target_page.url, parameter, client)
