""" This modules provides various attacks and functions to run them. """
from ..client import Client
from .xss import XssAttack

class Attack(object):
    """ Interace for other attacks. """
    def __init__(self, target_page):
        self.target_page = target_page
        # Because webvulnscan is a web vulnerability scanner, 
        # we generate a client.
        self.client = Client()
        
    def run(self):
        pass

class AttackDriver(object):
    def __init__(self):
        self.attacks = []

    def add_attack(self, attack):
        self.attacks.append(attack)

    def run(self, target_page):
        for attack in self.attacks:
            attack(target_page).run()

def drive_all(page):
    """ Drives every known attack against target. """
    driver = AttackDriver()
    # ...
    driver.add_attack(XssAttack)
    # ...
    driver.run(page)
