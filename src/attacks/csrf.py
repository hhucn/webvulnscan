from utils import get_plain_text, change_parameter

try:
    from http.cookiejar import CookieJar
except ImportError:
    from cookielib import CookieJar

def csrf(url, url_parameters, url_forms):
    # Generate new cookiejar
    my_cookie_jar = CookieJar()
    _ = get_plain_text(url, None, my_cookie_jar)

    for form in url_forms:
        if url_forms[form] == {}:
            to_send = None
        else:
            to_send = url_forms[form]
        try:
            site = get_plain_text(form, to_send)
            my_site = get_plain_text(form, to_send, my_cookie_jar)
        except:
            my_site = None

        if my_site == None:
            pass
        else:
            print("Vulnerability: CSRF under " + form)

