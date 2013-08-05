""" This modules provides is able to carry out a xss attack. """
from utils import get_plain_text, change_parameter

XSS_STRING = "<script>alert('Example');</script>"

def search_for_success(text, string):
    success = text.find(string)
    if success == -1:
        return False 
    else:
        return True


def find_get_xss(url, url_parameters):
    for parameter in url_parameters:
        new_url = change_parameter(url, parameter, XSS_STRING)

        try:
            site = get_plain_text(new_url)
        except:
            site = None

        if site == None:
            pass
        else:
            if search_for_success(site, XSS_STRING):
                print("Vulnerability: XSS on " + url + " in parameter " +
                    parameter)

def find_post_xss(url, url_forms):
    for form in url_forms:
        for parameter in url_forms[form]:
            current_parameters = url_forms[form]
            current_parameters[parameter] = XSS_STRING
            try:
                site = get_plain_text(form, current_parameters)
            except:
                site = None

            if site == None:
                pass
            else:
                if search_for_success(site, XSS_STRING):
                    print("Vulnerability: XSS on " + form + " in parameter " +
                        parameter)

def xss(url, url_parameters, url_forms):
    # Check for get parameters.
    find_get_xss(url, url_parameters)
    find_post_xss(url, url_forms)


