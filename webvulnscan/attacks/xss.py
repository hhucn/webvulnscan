from logging import getLogger

from ..client import Client
from ..utils import change_parameter

log = getLogger(__name__)
XSS_STRING = '<script>alert("XSS_STRING");'


class XssAttack(object):
    def __init__(self, page):
        self.target_page = page
        self.client = Client()

    def try_post_xss(self, form):
        # A helper function for modifing values of the parameter list.
        def modify_parameter(target_name, value):
            parameters = {x: y for x, y in form.get_inputs()}
            parameters[target_name] = value
            return parameters

        for parameter_name, parameter_value in form.get_inputs():
            # Replace value with XSS_STRING
            parameters = modify_parameter(parameter_name, XSS_STRING)

            # Send the form
            attacked_page = form.send(self.client, parameters)

            # Determine if the string is unfiltered on the page.
            if XSS_STRING in attacked_page.html:
                # Oh no! It is!
                log.warning("Vulnerability XSS under " + attacked_page.url +
                            " in parameter " + parameter_name)

    def try_get_xss(self, parameter):
        # copy the url.
        url = self.target_page.url
        # Replace the value of the parameter with XSS_STRING
        attack_url = change_parameter(url, parameter, XSS_STRING)
        # To run the attack, we just request the site.
        attacked_page = self.client.download_page(attack_url)
        # If XSS_STRING is found unfilitered in the site, we have a problem.
        if XSS_STRING in attacked_page.html:
            # Theres something wrong.
            log.warning("Vulnerability XSS under " + attacked_page.url +
                        " in URL parameter " + parameter)

    def run(self):
        # Iterate through the forms
        for form in self.target_page.get_forms():
            self.try_post_xss(form)

        # Iterate through the URL-Parameters, we don't need their values.
        for parameter, _ in self.target_page.get_url_parameters():
            self.try_get_xss(parameter)
