"""
Functions described here are for python 2/3 compability and other tasks.
"""

from sys import stdout, stderr

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
