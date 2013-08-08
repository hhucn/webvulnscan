""" This modules provides various attacks and functions to run them. """
from .XSS import xss
from .CSRF import csrf


def drive_all(url, parameters, forms):
    """ Drives every known attack against target. """
    xss(url, parameters, forms)
    csrf(url, forms)
