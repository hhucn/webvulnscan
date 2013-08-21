""" This modules provides various attacks and functions to run them. """
from .xss import xss
from .csrf import csrf
from .breach import breach
from .clickjack import clickjack
from .cookiescan import cookiescan
from .exotic_charaters import exotic_charaters
from .broken_unicode_characters import broken_unicode_characters


def AttackList():
    return [xss, csrf, breach, clickjack, cookiescan, exotic_charaters,
            broken_unicode_characters]


def drive_all(page, attacks, client):
    """ Drives every known attack against target. """

    for attack in attacks:
        attack(page, client)
