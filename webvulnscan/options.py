from optparse import OptionParser, OptionGroup, Values

from .attacks import all_attacks
from .utils import read_config


def parse_options():
    parser = OptionParser(usage='usage: %prog [options] url...')

    default_options = OptionGroup(parser, "Default", "")
    default_options.add_option('--verbose', '-v', default=None, dest="verbose",
                               action="store_true",
                               help="Print the current targets, etc.")
    default_options.add_option('--dont-filter', default=True, dest="do_print",
                               action="store_false",
                               help="Write output directly to the command"
                               "line, don't filter it.")
    default_options.add_option('--vulnerabilities-only', default=False,
                               dest="vuln_only", action="store_true",
                               help="Print only vulnerabilities "
                                    "(i.e. no warnings)")
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

#    filter_options = OptionGroup(parser, "Filter",
#                                 "Functions which may"
#                                 "enhance user experience")
#    filter_options.add_option("--no-heuristics",
#                              dest="no_heuristics"
#                              help="Do not filter results")
#    parser.add_option_group(filter_options)

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
