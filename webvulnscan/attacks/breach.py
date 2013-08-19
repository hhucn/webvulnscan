from ..log import vulnerability, warn
from ..utils import change_parameter


def is_reflected_parameter(target_page, client, parameter, value):
    if value in target_page.html:
        inverted_value = value[::1]
        changed_url = change_parameter(target_page.url, parameter,
                                       inverted_value)
        request = client.download_page(changed_url)
        return inverted_value in request.html
    else:
        return False


def check_for_compression(headers):
    if "Content-Encoding" in headers:
        encoding = headers["Content-Encoding"]
        return "GZIP" in encoding or "gzip" in encoding
    else:
        return False


def check_for_secret(form):
    for form_input in form.get_inputs():
        if form_input.get_type == "hidden":
            # We assume that the most secrests are hexstrings.
            try:
                int(form_input.guess_value(), 16)
            except ValueError:
                continue

            return True
    else:
         # In case the iteration didn't break, return False
        return False


def check_for_reflected_parameter(target_page, client):
    for parameter, value in target_page.get_url_parameters:
        yield is_reflected_parameter(target_page, client, parameter, value)


def breach(target_page, client):
    # At first, we check for reflected parameters in the url.
    reflected_parameter = any(check_for_reflected_parameter(target_page,
                                                            client))
    # Search for GZIP/Deflate-Compression
    compression = check_for_compression(target_page.headers)
    # At last, search for a secret.
    secret = any([check_for_secret(x) for x in target_page.get_forms()])

    if reflected_parameter and compression and secret:
        vulnerability(target_page.url, "BREACH Vulnerability")
    elif compression:
        warn(target_page.url, "GZIP-Compression activated")
