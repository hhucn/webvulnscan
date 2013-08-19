from inspect import currentframe, getouterframes

logging_messages = {}


def get_function_caller():
    current_frame = currentframe()
    calframe = getouterframes(current_frame)
    return calframe[3][3]


def log(group, message):
    global logging_messages

    if group in logging_messages:
        logging_messages[group].add(message)
    else:
        logging_messages.update({group: {message}})


def warn(target, vulnerability, msg=""):
    message = "Warning: " + target + " " + vulnerability + " " + msg
    log(vulnerability, message)


def vulnerability(target, vulnerability, msg=""):
    message = "Vulnerability: " + target + " " + vulnerability + " " + msg
    log(vulnerability, message)


def info(target, vulnerability, msg=""):
    print("Information: %s" % msg)
