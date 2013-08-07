""" This Module provides CSRF-Checking capabilities """
from ..utils import get_plain_text
from logging import getLogger

try:
    from http.cookiejar import CookieJar
except ImportError:
    from cookielib import CookieJar

try:
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import HTTPError

log = getLogger('log')


def csrf(url, url_forms):
    """
    Checks for Cross-Site-Request-Forgery vulnerabilities on the given
    site.
    """
    # Generate new cookiejar
    my_cookie_jar = CookieJar()
    get_plain_text(url, cookies=my_cookie_jar)

    for form, entries in url_forms.items():
        try:
            get_plain_text(form, entries)
            my_site = get_plain_text(form, entries, my_cookie_jar)
        except HTTPError:
            continue

        if my_site is None:
            log.warning("Vulnerability: CSRF under " + form)
