""" This modules provides is able to carry out a xss attack. """
from ..utils import get_plain_text, change_parameter

try:
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import HTTPError

try:
    from http.client import BadStatusLine
except ImportError:
    from httplib import BadStatusLine


XSS_STRING = "<script>alert('Example');</script>"


def search_for_success(text, string):
    """ Searchs for string in text and returns True if found. """
    return string in text


def find_get_xss(url, url_parameters):
    """ Searchs for XSS-Vulnerabilities in URLs. """
    for parameter in url_parameters:
        new_url = change_parameter(url, parameter, XSS_STRING)
        try:
            site = get_plain_text(new_url)
        except HTTPError:
            site = None

        if site is not None:
            if search_for_success(site, XSS_STRING):
                print("Vulnerability: XSS on " + url + " in parameter " +
                      parameter)


def find_post_xss(url_forms):
    """ Searchs for XSS-Vulnerabilties in POST-Request. """
    for form in url_forms:
        for parameter in url_forms[form]:
            current_parameters = url_forms[form]
            current_parameters[parameter] = XSS_STRING
            try:
                site = get_plain_text(form, current_parameters)
            except HTTPError:
                site = None
            except BadStatusLine:
                site = None

            if site is not None:
                if search_for_success(site, XSS_STRING):
                    print("Vulnerability: XSS on " + form + " in parameter " +
                          parameter)


def xss(url, url_parameters, url_forms):
    """ Checks for Cross-Site-Scripting in the given site. """
    # Check for get parameters.
    find_get_xss(url, url_parameters)
    find_post_xss(url_forms)
