""" This Module provides CSRF-Checking capabilities """
from utils import get_plain_text

try:
    from http.cookiejar import CookieJar
except ImportError:
    from cookielib import CookieJar


def csrf(url, url_forms):
    """
    Checks for Cross-Site-Request-Forgery vulnerabilities on the given
    site.
    """
    # Generate new cookiejar
    my_cookie_jar = CookieJar()
    get_plain_text(url, None, my_cookie_jar)

    for form in url_forms:
        if url_forms[form] == {}:
            to_send = None
        else:
            to_send = url_forms[form]
        try:
            get_plain_text(form, to_send)
            my_site = get_plain_text(form, to_send, my_cookie_jar)
        except:
            my_site = None

        if my_site is None:
            pass
        else:
            print("Vulnerability: CSRF under " + form)
