from ..utils import attack, change_parameter, could_be_secret


def check_for_compression(headers, field='Content-Encoding'):
    v = headers.get(field, 'identity').split(',')
    gzip = 'gzip' not in (e.strip().lower() for e in v)
    deflate = 'deflate' not in (e.strip().lower() for e in v)
    return gzip or deflate


def find_secrets(form):
    return set(
        (form_input.get_name, form_input.get_element_value)
        for form_input in form.get_inputs()
        if (form_input.get_type == "hidden"
            and could_be_secret(form_input.get_element_value)))


@attack()
def breach(client, log, target_page):
    if not check_for_compression(target_page.request.headers,
                                 'Accept-Encoding'):
        # Redownload with request for gzip
        new_request = target_page.request.copy()
        new_request.headers['Accept-Encoding'] = "deflate, gzip"
        target_page = client.download_page(request)
    if not check_for_compression(target_page.headers):
        return

    secrets = dict((form.action, find_secrets(form))
                   for form in target_page.get_forms())

    page_redownload = client.download_page(target_page.request)
    for form in page_redownload.get_forms():
        redownload_secrets = find_secrets(form)
        previous_secrets = secrets[form.action]
        constant_secrets = previous_secrets.intersection(redownload_secrets)
        if constant_secrets:
            log('vuln', target_page.url, u'BREACH vulnerability',
                u'Secrets %r do not change during redownload'
                % dict(constant_secrets),
                request=target_page.request)
