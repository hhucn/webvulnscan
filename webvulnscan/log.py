EXIT_CODE = 0


def warn(msg=""):
    print("Warning: %s" % msg)
    global EXIT_CODE
    EXIT_CODE = 1


def vulnerability(msg=""):
    print("Vulnerability: %s" % msg)
    global EXIT_CODE
    EXIT_CODE = 1


def info(msg=""):
    print("Information: %s" % msg)
