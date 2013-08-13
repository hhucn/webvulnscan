""" This modules provides various attacks and functions to run them. """
from ..client import Client
from .xss import XssAttack
from .csrf import CsrfAttack
from .breach import BreachAttack


class Attack(object):
    """ Interace for other attacks. """
    def __init__(self, target_page):
        self.target_page = target_page
        # Because webvulnscan is a web vulnerability scanner,
        # we generate a client.
        self.client = Client()

    def run(self):
        pass


def AttackList():
    return [XssAttack, CsrfAttack, BreachAttack]


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
    if attacks is None:
        attacks = AttackList()

    driver = AttackDriver(client)

    for attack in attacks:
        driver.add_attack(attack)

    driver.run(page)
