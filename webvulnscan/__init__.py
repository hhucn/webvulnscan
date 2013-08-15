""" Main module provides crawling functions and user interface """
from optparse import OptionParser, OptionGroup

from .utils import read_config, write_config

from .crawler import Crawler
from .client import Client
from .utils import get_url_host
from .attacks import drive_all, AttackList

import webvulnscan.log


def run(options, arguments):
    attacks = []

    for attack in AttackList():
        if attack.__name__ in options.__dict__:
            attacks.append(attack)

    if not attacks:
        attacks = AttackList()

    client = Client()

    if options.auth_url is not None and options.auth_data is not None:
        post_data = {}

        for field in options.auth_data:
            name, _, value = field.partition('=')
            post_data.update({name: value})

            _, text, _ = client.download(options.auth_url, post_data)

    for target in arguments:

        host = get_url_host(target)
        options.white_list.add(host)

        if options.no_crawl:
            urls = [target]
        else:
            urls = Crawler(target, options.white_list, client,
                           options.blacklist)
            for page in urls:
                if options.verbose:
                    print("Scanning " + page.url)

                drive_all(page, attacks, client)

    global EXIT_CODE
    exit(webvulnscan.log.EXIT_CODE)


def main():
    parser = OptionParser(usage='usage: %prog [options] http(s)://target/ '
                                '[http(s)://another.target/]')

    default_options = OptionGroup(parser, "Default", "")

    default_options.add_option('--verbose', '-v', default=None, dest="verbose",
                               action="store_true",
                               help="Print the current targets, etc.")

    parser.add_option_group(default_options)

    crawling_options = OptionGroup(parser, "Crawling",
                                   "This section provides information"
                                   "about the different crawling options.")

    crawling_options.add_option('--no-crawl', action='store_true',
                                dest='no_crawl',
                                help="DO NOT search for links on the target")

    crawling_options.add_option('--whitelist', default=set(),
                                dest="white_list",
                                help="Hosts which are allowed to be crawled.")
    crawling_options.add_option('--blacklist', default=[], dest="blacklist",
                                action="append",
                                help="Specify sites which shouldn't be"
                                "visited or attacked. (Hint: logout)")

    parser.add_option_group(crawling_options)

    authentification_options = OptionGroup(parser, "Authentification",
                                           "Authentification to a specific"
                                           " post site.")
    authentification_options.add_option('--auth',  default=None,
                                        dest="auth_url",
                                        help="Post target for "
                                        "authentification")

    authentification_options.add_option('--auth-data',  dest='auth_data',
                                        action='append', type='str',
                                        default=[],
                                        help="A post parameter in the "
                                        "form of targetname=targetvalue")

    parser.add_option_group(authentification_options)

    configuration_options = OptionGroup(parser, "Configuration",
                                        "You are also able to write your"
                                        " specified parameters in a file"
                                        " for easier usage.")

    configuration_options.add_option('--config', '-c', default="",
                                     dest="read_config",
                                     help="Read the parameters from FILE")

    configuration_options.add_option('--write-out', default="",
                                     dest="write_config",
                                     help="Insted of running the options,"
                                     " write them to the specified file. ")

    parser.add_option_group(configuration_options)

    # Options for scanning for specific vulnerabilities.
    attack_options = OptionGroup(parser, "Attacks",
                                 "If you specify own or several of the "
                                 "options _only_ this/these will be run. "
                                 "If you don't specify any, all will be "
                                 "run.")
    for attack in AttackList():
        attack_options.add_option('--' + attack.__name__, dest=attack.__name__,
                                  action="store_true", default=False)

    parser.add_option_group(attack_options)

    options, arguments = parser.parse_args()

    if options.write_config:
        write_config(options.write_config, options, arguments, parser)
        exit()

    if options.read_config:
        options, arguments = read_config(options.read_config, parser)

    run(options, arguments)
