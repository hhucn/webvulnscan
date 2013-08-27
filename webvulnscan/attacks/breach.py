from ..utils import attack, change_parameter, could_be_secret


def is_reflected_parameter(target_page, client, parameter, value):
    inverted_value = "test"
    changed_url = change_parameter(target_page.url, parameter,
                                   inverted_value)
    request = client.download_page(changed_url)
    return inverted_value in request.html


def check_for_compression(headers):
    if "Content-Encoding" in headers:
        encoding = headers["Content-Encoding"]
        return "GZIP" in encoding or "gzip" in encoding
    else:
        return False


def find_secrets(form):
    return set(
        (form_input.get_name, form_input.get_element_value)
        for form_input in form.get_inputs()
        if (form_input.get_type == "hidden"
            and could_be_secret(form_input.get_element_value)))


@attack()
def breach(client, log, target_page):
    if not check_for_compression(target_page.headers):
        return

    secrets = dict((form.get_action, check_for_secret(form))
                   for form in target_page.get_forms())

    page_redownload = client.download_page(target_page)
    for form in page_redownload.get_forms():
        redownload_secrets = find_secrets(form)
        constant_secrets = secrets[form].intersection(redownload_secrets)
        if constant_secrets:
            log('vuln', target_page.url, "BREACH Vulnerability",
                'Secrets %r do not change during redownload' % double_secrets)
