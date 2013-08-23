from optparse import OptionParser, OptionGroup, Values
import signal
import sys

from .utils import read_config, write_config

from .crawler import Crawler
from .client import Client
from .utils import get_url_host
from .attacks import drive_all, all_attacks
from .compat import MozillaCookieJar

import webvulnscan.log
from .log import logging_messages


def print_logs(target="", crawled_pages=0):
    if logging_messages:
        for name, value in logging_messages.items():
            for sub_name in sorted(value.keys()):
                sub_value = value[sub_name]
                if len(logging_messages[name][sub_name]) == crawled_pages:
                    if "Warning: " in sub_value.pop():
                        print("Warning:" + target + "*" + " " + sub_name)
                    else:
                        print("Vulnerability: " + target +
                              "*" + " " + sub_name)
                else:
                    for entry in sub_value:
                        print(str(entry))


def run(options, targets):
    options.whitelist = set(options.whitelist)
    options.blacklist = set(options.blacklist)

    webvulnscan.log.do_print = options.verbose
    webvulnscan.log.abort_early = options.abort_early
    webvulnscan.log.very_verbose = options.very_verbose

    attacks = []
    for attack in all_attacks():
        if options.__dict__[attack.__name__]:
            attacks.append(attack)

    if not attacks:
        attacks = all_attacks()

    for attack in attacks:
        except_attack = options.__dict__[attack.__name__ + "_except"]

        if not except_attack:
            continue

        attacks.remove(attack)

    client = Client()

    if options.import_cookies:
        client.cookie_jar = MozillaCookieJar(options.import_cookies)
        client.cookie_jar.load()

    # TODO This is horrible. Remove it!
    if options.auth_url is not None and options.auth_data is not None:
        post_data = {}

        for field in options.auth_data:
            name, _, value = field.partition('=')
            post_data.update({name: value})

            _, text, _ = client.download(options.auth_url, post_data)
    elif options.form_page and options.form_id:
        form_data = {}

        for field in options.form_data:
            name, _, value = field.partition('=')
            form_data.update({name: value})

        form_page = client.download_page(options.form_page)
        print([x.document.attrib.get('id') for x in form_page.get_forms()])
        form = [x for x in form_page.get_forms()
                if x.document.attrib.get('id') == options.form_id][0]

        entries = dict(form.get_parameters())

        for option, value in form_data.items():
            entries[option] = value

        form.send(client, entries)

    for target in targets:
        crawled_pages = 0

        host = get_url_host(target)
        options.whitelist.add(host)

        if options.no_crawl:
            urls = [client.download_page(target)]
        else:
            urls = Crawler(target, options.whitelist, client,
                           options.blacklist)

        for page in urls:
            if options.verbose:
                print("Scanning " + page.url)

            drive_all(page, attacks, client)
            crawled_pages += 1

        print_logs(target, crawled_pages)

    return logging_messages


def parse_options():
    parser = OptionParser(usage='usage: %prog [options] url...')

    default_options = OptionGroup(parser, "Default", "")
    default_options.add_option('--verbose', '-v', default=None, dest="verbose",
                               action="store_true",
                               help="Print the current targets, etc.")
    default_options.add_option('--very-verbose', '--vv', default=False,
                               dest="very_verbose", action="store_true",
                               help="Print every")
    default_options.add_option('--dont-filter', default=False, dest="do_print",
                               action="store_true",
                               help="Write output directly to the command"
                               "line, don't filter it.")
    default_options.add_option('--abort-early', '-a', default=False,
                               dest="abort_early", action="store_true",
                               help="Exit on first found vulnerability.")
    default_options.add_option('--import-cookies', default=None,
                               dest="import_cookies",
                               help="Given a file, it will import it."
                               "(Hint: Useful to avoid Captchas...)")
    parser.add_option_group(default_options)

    crawling_options = OptionGroup(parser, "Crawling",
                                   "This section provides information"
                                   "about the different crawling options.")
    crawling_options.add_option('--no-crawl', action='store_true',
                                dest='no_crawl',
                                help="DO NOT search for links on the target")
    crawling_options.add_option('--whitelist', default=[],
                                dest="whitelist",
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
    authentification_options.add_option('--form-page', dest='form_page',
                                        default=None,
                                        help="The site of the form you want "
                                        "to use to sign in")
    authentification_options.add_option('--form-id', dest='form_id',
                                        default=None,
                                        help="The id of the form you want "
                                        "to use to sign in.")
    authentification_options.add_option('--form-data', dest='form_data',
                                        action='append', type='str',
                                        default=[],
                                        help="A field you want to set "
                                        "manually.")
    parser.add_option_group(authentification_options)

    configuration_options = OptionGroup(parser, "Configuration",
                                        "You are also able to write your"
                                        " specified parameters in a file"
                                        " for easier usage.")
    configuration_options.add_option('--config', '-c', metavar='FILE',
                                     dest="read_config",
                                     help="Read the parameters from FILE")
    configuration_options.add_option('--write-config', metavar='FILE',
                                     dest="write_config",
                                     help="Insted of running the options,"
                                     ' write them to the specified file ("-" '
                                     'for standard output).')
    parser.add_option_group(configuration_options)

    # Options for scanning for specific vulnerabilities.
    attack_options = OptionGroup(parser, "Attacks",
                                 "If you specify own or several of the "
                                 "options _only_ this/these will be run. "
                                 "If you don't specify any, all will be "
                                 "run.")
    for attack in all_attacks():
        attack_options.add_option('--' + attack.__name__, dest=attack.__name__,
                                  action="store_true", default=False)
        attack_options.add_option('--except-' + attack.__name__,
                                  dest=attack.__name__ + "_except",
                                  action="store_true", default=False)
    parser.add_option_group(attack_options)

    # Get default values
    options, arguments = parser.parse_args([])

    # Parse command line
    cli_options = Values()
    _, cli_arguments = parser.parse_args(values=cli_options)

    # Update default values with configuration file
    config_fn = cli_options.__dict__.get('read_config')
    if config_fn is not None:
        read_options, read_arguments = read_config(config_fn, parser)
        options.__dict__.update(read_options)
        arguments += read_arguments

    # Update actual CLI options
    options.__dict__.update(cli_options.__dict__)
    arguments += cli_arguments

    if not arguments and not options.write_config:
        parser.error(u'Need at least one target')

    return (options, arguments)


def main():
    # Handle SIGPIPE (sent when someone is processing our output and is done)
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)

    options, arguments = parse_options()

    if options.write_config:
        write_config(options.write_config, options, arguments)
        sys.exit(0)

    try:
        messages = run(options, arguments)
    except KeyboardInterrupt:
        sys.exit(130)
    except SystemExit:
        print_logs()
        sys.exit(1)
    except BaseException:
        print_logs()
        raise

    if messages:
        sys.exit(1)
