from utils import print_msg, print_err, print_vuln, unrelative_link
from optparse import OptionParser
from sys import version_info, exit
import xml.etree.ElementTree as ET
import re

try:
    from urllib.request import urlopen 
except ImportError:
    from urllib2 import urlopen

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin 


def crawl(html):
    """ Takes a html string and returns a list of strings. """
    decoded_html = html.decode("utf-8")

    # REMOVE DOCTYPE
    if decoded_html.startswith("<!doctype"):
        _, _, decoded_html  = decoded_html.partition('>')


    # Can't take XML any longer, TODO replace it with real entity removing.
    parser = ET.XMLParser()
    parser.entity["Ouml"] = ""
    parser.entity["Auml"] = ""
    parser.entity["Uuml"] = ""
    parser.entity["ouml"] = ""
    parser.entity["auml"] = ""
    parser.entity["uuml"] = ""


    try:
        root = ET.fromstring(decoded_html, parser)
        
    except ET.ParseError as e:
        print("The follow line contains invalid XML:")
        print(decoded_html.split('\n')[e.position[0]])
        exit(2)
    
    return [link.attrib.get('href') for link in root.findall('.//a[@href]')]

        

#def form_crawl(html):
#    """ 
#    Takes a html string a dictionariy with the different forms 
#    and their parameters.
#    """
#    form_position = html.find('<form')
#    forms = list()
#    return_list = {}

#    while form_position != -1:
#        form_close = html.find('</form>', form_position)
#        forms.extend([html[form_position:form_close]])
#        form_position = html.find('<form', form_close)

#    for form in forms:
#        close_tag       = form.find('>')
#        action_position = form.find('action=') + len('action=')
#        action          = unquote(form[action_position:close_tag])
#        inputs          = form.split('<input')[1:]
#        entry           = {action: {}}


#        for field in inputs:
#            field_name = unquote(field[field.find('name=') + len('name='):])
#            field_type = unquote(field[field.find('type=') + len('type='):])
#            value      = unquote(field[field.find('value=') + len('value='):])
            # The data is not submitted so it is unintresting.
#            if field_type == 'submit':
#                pass
#            else:
#                entry[action].update({field_name:(field_type, value)})

#        return_list.update(entry)

#    return return_list
    
def get_page(url):
    response = urlopen(url)
    return response.read()

def crawl_page(url, already_visited=[]):
    html = get_page(url)

#    significant_forms = dict()
#    forms = form_crawl(html)
#    for form in forms:
#        form_link = urljoin(url, form)
#        if form_link not in already_visited:
#            already_visited.extend([form_link])
#            significant_forms.update({form_link:forms[form]})

    for link in crawl(html):
        link = urljoin(url, link)
        if link not in already_visited:
            already_visited.extend([link])
            crawl_page(link, already_visited)

    drive_attack(url, {})

def drive_attack(url, url_forms):
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
