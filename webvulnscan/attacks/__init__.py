""" This modules provides various attacks and functions to run them. """
from .xss import xss
from .csrf import csrf
from .breach import breach

def AttackList():
    return [xss, csrf, breach]


class AttackDriver(object):
    def __init__(self, client):
        self.attacks = []
        self.client = client

    def add_attack(self, attack):
        self.attacks.append(attack)

    def run(self, target_page):
        for attack in self.attacks:
            attack(target_page).run(self.client)


def drive_all(page, attacks, client):
    """ Drives every known attack against target. """

    for attack in attacks:
        attack(page, client)
