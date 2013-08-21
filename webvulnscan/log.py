logging_messages = {0: {}, 1: {}}
do_print = False  # For debugging
very_verbose = False


def log(level, group, message):
    global logging_messages

    if group in logging_messages[level]:
        logging_messages[level][group].add(message)
    else:
        logging_messages[level].update({group: {message}})


def warn(target, vulnerability, msg=""):
    message = "Warning: " + target + " " + vulnerability + " " + msg

    if do_print:
        print(message)
    else:
        log(0, vulnerability, message)


def vulnerability(target, vulnerability, msg=""):
    message = "Vulnerability: " + target + " " + vulnerability + " " + msg

    if do_print:
        print(message)
    else:
        log(1, vulnerability, message)


def info(target, msg=""):
    print("Information: " + target + " " + msg)
