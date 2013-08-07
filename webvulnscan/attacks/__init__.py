""" This modules provides various attacks and functions to run them. """
from .xss import xss
from .csrf import csrf


def drive_all(url, parameters, forms):
    """ Drives every known attack against target. """
    xss(url, parameters, forms)
    csrf(url, forms)
