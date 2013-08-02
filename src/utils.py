"""
Functions described here are for python 2/3 compability and other tasks.
"""

from sys import stdout, stderr

def unrelative_link(current_page, link):
    """ Similar to urlparse.urljoin """
    if link[0] == "/":
        host_begins = current_page.find('://') + 3
        host_ends   = current_page.find('/', host_begins) 
        return current_page[:host_ends] + link
    elif "://" in link:
        return link
    else:
        slash_count = link.count('/')
        before, slash, _ = link.rpartition('/')
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

def print_msg(message):
    """ Prints str(message) as a line.

    """
    stdout.write(str(message) + "\n")

def print_vuln(vulnerability):
    """ Should  print the vulnerability """
    pass

def print_err(error, dramatic=True):
    """ Prints a error and exists if dramatic is set. """
    stderr.write(str(error) + "\n")

    if dramatic:
        exit(2)
