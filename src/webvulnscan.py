from utils import print_msg, print_err, print_vuln
from optparse import OptionParser


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
        inputs          = form.split('</input>')
        entry           = {action: {}}

        for field in inputs:
            field_name = unquote(field[field.find('name=') + len('name='):])
            field_type = unquote(field[field.find('type=') + len('type='):])
            entry[action].update({field_name:field_type})

        return_list.update(entry)

    return return_list
        

def main():
    """ The main function. """
    parser = OptionParser()

    parser.add_option('--target', '-t', help="URL of the target")
    parser.add_option('--crawl', action="store_false", dest="crawl", 
        help="search for links on the target")

    options, arguments = parser.parse_args()
   

if __name__ == '__main__':
    main()
