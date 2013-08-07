from utils import get_page, get_url_host

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

try:
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import HTTPError

try:
    from http.client import BadStatusLine
except ImportError:
    from httplib import BadStatusLine


def links_on_site(url, document):
    if document is not None:
        for link in document.findall('.//a[@href]'):
            href = link.attrib.get('href')
            yield urljoin(url, href)


def inputs_in_form(form):
    for input in form.findall('.//input[@type]'):
        input_name = input.attrib.get('name')
        input_type = input.attrib.get('type')
        if input_type != "submit":
            yield input_name, input_type


def forms_on_site(url, document):
    for form in document.findall('.//form[@action]'):
        target = urljoin(url, form.attrib.get('action'))
        inputs = {x: y for x, y in inputs_in_form(form)}
        yield target, inputs


def crawl(url, whitelist, already_visited=None):
    if already_visited is None:
        already_visited = set()

    if get_url_host(url) not in whitelist:
        yield None, None

    html = get_page(url)

    if html is None:
        yield None, None
    else:
        significant_forms = dict()
        forms = {x: y for x, y in forms_on_site(url, html)}
        for form in forms:
            if form not in already_visited:
                already_visited.update({form})
                significant_forms.update({form: forms[form]})

        yield url, significant_forms

        for link in links_on_site(url, html):
            if link not in already_visited:
                already_visited.update({link})
                for url, forms in crawl(link, whitelist, already_visited):
                    if url is not None and forms is not None:
                        yield url, forms
# TODO übernehme von https://github.com/SysTheron/webvulnscan/commit/c94cfa837efbf45fb7c04511187064941d0bd48f
