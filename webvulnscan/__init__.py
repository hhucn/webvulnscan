import signal
import sys

from .attacks import all_attacks
from .client import Client
from .compat import MozillaCookieJar, urlparse
from .crawler import Crawler
from .log import Log
from .options import parse_options
from .utils import get_url_host
from .utils import write_config


def run(options, targets):
    options.whitelist = set(options.whitelist)
    options.blacklist = set(options.blacklist)

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

    if options.verbose:
        log = Log(verbosity='info', direct_print=True)
    elif options.vuln_only:
        log = Log(verbosity=u'vuln')
    else:
        log = Log()
    client = Client(log=log)

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
        form = [x for x in form_page.get_forms()
                if x.document.attrib.get('id') == options.form_id][0]

        entries = dict(form.get_parameters())

        for option, value in form_data.items():
            entries[option] = value

        form.send(client, entries)

    try:
        for target in targets:
            if not urlparse(target).scheme:
                target = u'http://' + target

            options.whitelist.add(get_url_host(target))

            if options.no_crawl:
                all_pages = [client.download_page(target)]
            else:
                all_pages = Crawler(target, options.whitelist, client,
                                    options.blacklist)

            for page in all_pages:
                log('info', page.url, 'crawler', 'Scanning ...')

                for attack in attacks:
                    attack(client, log, page)

    finally:
        if not options.verbose:
            log.print_report(summarize=options.do_print)


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
        sys.exit(1)
    except BaseException:
        raise

    if messages:
        sys.exit(1)
