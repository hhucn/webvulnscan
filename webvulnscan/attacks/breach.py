from logging import getLogger

from ..client import Client
from ..utils import change_parameter

log = getLogger(__name__)


class BreachAttack(object):
    name = "breach"

    def __init__(self, target_page):
        self.client = Client()
        self.log = log
        self.target_page = target_page

    def check_for_reflected_parameter(self, parameter, value):
        if value in self.target_page.html:
            inverted_value = value[::-1]
            changed_url = change_parameter(self.target_page.url,
                                           parameter, inverted_value)
            request = self.client.download_page(changed_url)
            if inverted_value in request.html:
                return True
            else:
                return False

    def check_for_compression(self, headers):
        if "Content-Encoding" in headers:
            encoding = headers["Content-Encoding"]
            if "GZIP" in encoding or "gzip" in encoding:
                return True
            else:
                return False
        else:
            return False

    def check_for_secret(self, form):
        for form_input in form.get_inputs():
            if form_input.get_type() == "hidden":
                # We assume that the most secrests are hexstrings.
                try:
                    int(form_input.guess_value(), 16)
                    secret = True
                except ValueError:
                    # In this case, it isn't a hex string.
                    secret = False

                return secret

        # In case the iteration didn't break, return False
        return False

    def run(self):
        # At first, we check for reflected parameters in the url.
        reflected_url = False

        for parameter, value in self.target_page.get_url_parameters():
            reflected_url = self.check_for_reflected_parameter(parameter,
                                                               value)

        # Search for GZIP/Deflate-Compression
        compression = self.check_for_compression(self.target_page.headers)

        # At last, search for a secret.
        secret = False
        for form in self.target_page.get_forms():
            secret = self.check_for_secret(form)

        if reflected_url and compression and secret:
            self.log.warning("Vulnerability: BREACH Vulnerability under " +
                             self.target_page.url)
        elif compression:
            self.log.warning("Warning: GZIP-Compression activated under " +
                             self.target_page.url)
