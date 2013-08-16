from ..log import vulnerability
from ..compat import urlparse


def check_for_forms(page):
    return page.get_forms() is not None


def check_for_links(page):
    return page.get_links() is not None


def is_valid(frame_options):
    if frame_options == "DENY":
        return True

    if frame_options == "SAME-ORIGIN":
        return True

    first_word, _, url = frame_options.partition(" ")
    if first_word == "ALLOW-FROM":
        netloc = urlparse(url).netloc
        if netloc:
            return True

    return False


def clickjack(page, client):
    content_type = page.headers["Content-Type"]

    if "text/html" in content_type or content_type is None:
        return

    clickable_content = check_for_forms(page) or check_for_links(page)

    if clickable_content:
        if "X-Frame-Options" in page.headers:
            frame_options = page.headers["X-Frame-Options"]
        else:
            vulnerability("Clickjacking under " + page.url +
                          " no X-Frame-Options!")
            return

        if is_valid(frame_options):
            return
        else:
            vulnerability("Clickjacking under " + page.url +
                          " invalid X-Frame-Options!")
