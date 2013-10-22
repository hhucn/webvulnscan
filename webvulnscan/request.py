import copy
import sys

from . import compat
from .compat import urlencode, parse_qs


class Request(compat.Request):
    def __init__(self, url, parameters=None, headers=None):
        self.parameters = parameters
        if parameters is None:
            data = None
        else:
            if sys.version_info >= (3, 0):
                data = urlencode(parameters).encode('utf-8')
            else:
                byte_parameters = dict(
                    (k.encode('utf-8'), v.encode('utf-8'))
                    for k, v in parameters.items())
                data = urlencode(byte_parameters)
            assert isinstance(data, bytes)
        if headers is None:
            headers = {}
        compat.Request.__init__(self, url, data, headers)

    def copy(self):
        return copy.copy(self)

    @property
    def url(self):
        return self.get_full_url()
