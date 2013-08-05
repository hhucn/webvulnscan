""" This modules provides various attacks and functions to run them. """
from attacks.xss import xss


def drive_all(url, forms, parameters):
    """ Drives every known attack against target. """
    xss(url, forms, parameters)
