from utils import get_page
from optparse import OptionParser

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin 

try:
    from html.parser import HTMLParser
except ImportError:
    from htmlparser import HTMLParser


def crawl(document):
    """ Takes a html string and returns a list of strings. """
    link_list = []
    for link in document.findall('.//a[@href]'):
        link_target = link.attrib.get('href')
        link_list.extend([link_target])

    return link_list

        

def form_crawl(document):
    """ 
    Takes a html string a dictionariy with the different forms 
    and their parameters.
    """
    form_dict = {}
    for form in document.findall('.//form[@action]'):
        target = form.attrib.get('action')
        method = form.attrib.get('method')
        input_list = {}

        for sub_element in list(form):
            if sub_element.tag == "input":
                input_type = sub_element.attrib.get('type')
                input_name = sub_element.attrib.get('name')
                input_value = sub_element.attrib.get('value')

                input_list.update({input_name: (input_type, input_value)})

        form_dict.update({target: (method, input_list)})

    return form_dict

    
def crawl_page(url, already_visited=[]):
    """ Crawls url for its forms and links and attacks all. """
    # TODO: iterative, not recursive variant!
    html = get_page(url)

    if html == None:
        drive_attack(url, {})
    else:
        significant_forms = dict()
        forms = form_crawl(html)
        for form in forms:
            form_link = urljoin(url, form)
            if form_link not in already_visited:
                already_visited.extend([form_link])
                significant_forms.update({form_link:forms[form]})



        for link in crawl(html):
            link = urljoin(url, link)
            if link not in already_visited:
                already_visited.extend([link])
                crawl_page(link, already_visited)

        drive_attack(url, significant_forms)

def drive_attack(url, url_forms):
    """ Initates attack on the given target """
    print(url)
    print(url_forms)

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
