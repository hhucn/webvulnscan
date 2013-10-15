import copy

from . import compat
from .compat import urlencode, parse_qs


class Request(compat.Request):
    def __init__(self, url, parameters=None, headers=None):
        self.parameters = parameters
        if parameters is None:
            data = None
        else:
            byte_parameters = dict(
                (k.encode('utf-8'), v.encode('utf-8'))
                for k, v in parameters.items())
            data = urlencode(byte_parameters)
        if headers is None:
            headers = {}
        compat.Request.__init__(self, url, data, headers)

    def copy(self):
        return copy.copy(self)

    @property
    def url(self):
        return self.get_full_url()
