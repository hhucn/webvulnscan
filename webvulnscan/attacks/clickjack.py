from ..compat import urlparse
from ..utils import attack


def check_for_post_forms(page):
    return any(form
               for form in page.get_forms()
               if form.method == 'post')


def is_valid_header(frame_options):
    if frame_options == "DENY":
        return True

    if frame_options == "SAMEORIGIN":
        return True

    first_word, _, url = frame_options.partition(" ")
    if first_word == "ALLOW-FROM":
        netloc = urlparse(url).netloc
        if netloc:
            return True

    return False


@attack()
def clickjack(client, log, page):
    if 'Content-Type' in page.headers:
        content_type = page.headers['Content-Type']
    else:
        content_Type = ""

    if not check_for_post_forms(page):
        return  # No active content, so it's fine

    frame_options = page.headers.get('X-Frame-Options')
    if not frame_options:
        log('vuln', page.url, u'Clickjacking', u'no X-Frame-Options header')
        return

    if not is_valid_header(frame_options):
        log('vuln', page.url, u'Clickjacking', u'invalid X-Frame-Options!')
