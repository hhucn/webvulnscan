"""
Functions described here are for python 2/3 compability and other tasks.
"""

from ast import literal_eval
from .compat import urlparse, parse_qsl, urlunparse, urlencode, \
    RawConfigParser


class DictObj(dict):
    def __getattr__(self, attr):
        return self[attr]


def extended_eval(item):
    if item == "set()":
        return set()
    elif item == "":
        return ""
    else:
        try:
            return literal_eval(item)
        except ValueError:
            return item


def read_config(config_file, parser):
    config = RawConfigParser()
    config.read(config_file)

    arguments = []
    options = DictObj()

    for target in config.items("targets"):
        arguments.append(target[1])

    for option_group in parser.option_groups:
        section_name = option_group.title
        for option in option_group.option_list:
            item = config.get(section_name, option.dest)
            value = extended_eval(item)
            options[option.dest] = value

    return options, arguments


def write_config(filename, options, arguments, parser):
    config = RawConfigParser()
    config.add_section("targets")

    for count, item in enumerate(arguments):
        config.set("targets", str(count), item)

    for option_group in parser.option_groups:
        section_name = option_group.title
        config.add_section(section_name)
        for option in option_group.option_list:
            option_name = option.dest
            config.set(section_name, option_name,
                       options.__dict__[option_name])

    out_file = open(filename, "w+")
    config.write(out_file)


def find_parameter_values(url):
    """ Find the values of the parameters of the URL """
    if "?" in url:
        url = url.split("?")[1]

    url_parts = parse_qsl(url)

    for parameter in url_parts:
        yield parameter[1]


def change_parameter(url, parameter, new_value):
    """ Returns a new url where the parameter is changed. """
    url_parts = list(urlparse(url))
    query = parse_qsl(url_parts[4])
    for i in range(len(query)):
        entry = query[i]
        if entry[0] == parameter:
            query[i] = (entry[0], new_value)

    url_parts[4] = urlencode(query)
    return urlunparse(url_parts)


def get_url_host(url):
    """ Returns the server of a name."""
    parsed = urlparse(url)
    return parsed.netloc
