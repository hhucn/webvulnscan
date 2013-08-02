from utils import print_msg, print_err, print_vuln
from optparse import OptionParser
from sys import version_info

if version_info.major == 2:
    import urllib2
    urlopen = urllib2.urlopen
elif version_info.major == 3:
    import urllib.request
    urlopen = urllib.request.urlopen 
else:
    print_err("Your Python version isn't supported")

def unquote(quote):
    if quote[0] == '"':
        last_quote = quote.find('"', 1)
        return quote[1:last_quote]

    elif quote[0] == "'":
        last_quote = quote.find("'", 1)
        return quote[0:last_quote]

    else:
        # Somebody was lazy with his HTML...
        url_end = quote.find(' ', 0)

        if url_end == -1:
            return quote 
        else:
            return quote[:url_end]

def unrelative_link(current_page, link):
    """ Similar to urlparse.urljoin """
    if link[0] == "/":
        host_begins = current_page.find('://') + 3
        host_ends   = current_page.find('/', host_begins) 
        return current_page[:host_ends] + link
    elif "://" in link:
        return link
    else:
        last_slash  = 0
        slash_count = 0
        i = 0
        for char in current_page:
            if char == '/':
                last_slash = i
                slash_count += 1

            i += 1

        if slash_count == 3:
            return current_page + link
        else:
            return current_page[:last_slash+1] + link


def crawl(html):
    """ Takes a html string and returns a list of strings. """
    link_position = html.find('<a')
    link_list     = list()

    while link_position != -1:
        close_tag = html.find('>', link_position)
        href = html.find('href=', link_position, close_tag) + len('href=')

        link_list += [unquote(html[href:close_tag])]

        link_position = html.find('<a', close_tag)

    return link_list

def form_crawl(html):
    """ 
    Takes a html string a dictionariy with the different forms 
    and their parameters.
    """
    form_position = html.find('<form')
    forms = list()
    return_list = {}

    while form_position != -1:
        form_close = html.find('</form>', form_position)
        forms.extend([html[form_position:form_close]])
        form_position = html.find('<form', form_close)

    for form in forms:
        close_tag       = form.find('>')
        action_position = form.find('action=') + len('action=')
        action          = unquote(form[action_position:close_tag])
        inputs          = form.split('<input')[1:]
        entry           = {action: {}}


        for field in inputs:
            field_name = unquote(field[field.find('name=') + len('name='):])
            field_type = unquote(field[field.find('type=') + len('type='):])
            value      = unquote(field[field.find('value=') + len('value='):])
            # The data is not submitted so it is unintresting.
            if field_type == 'submit':
                pass
            else:
                entry[action].update({field_name:(field_type, value)})

        return_list.update(entry)

    return return_list
    
def get_page(url):
    response = urlopen(url)
    return str(response.read())

def crawl_page(url, already_visited=[]):
    html = get_page(url)

    significant_forms = dict()
    forms = form_crawl(html)
    for form in forms:
        form_link = unrelative_link(url, form)
        if form_link not in already_visited:
            already_visited.extend([form_link])
            significant_forms.update({form_link:forms[form]})

    for link in crawl(html):
        link = unrelative_link(url, link)
        if link not in already_visited:
            already_visited.extend([link])
            crawl_page(link, already_visited)

    drive_attack(url, significant_forms)

def drive_attack(url, url_forms):
    print_msg(url)
    print_msg(url_forms)




def main():
    """ The main function. """
    parser = OptionParser()

    parser.add_option('--target', '-t', help="URL of the target")
    parser.add_option('--crawl', action="store_true", dest="crawl", 
        help="search for links on the target")

    options, arguments = parser.parse_args()

    crawl_page(options.target)
        


if __name__ == '__main__':
    main()
